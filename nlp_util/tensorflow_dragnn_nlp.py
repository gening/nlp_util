# coding: utf-8

"""
Utility Tools for Tensorflow SyntaxNet: DRAGNN
==============================================
For installation: 
https://github.com/tensorflow/models/tree/master/syntaxnet

For demo: 
https://github.com/tensorflow/models/blob/master/syntaxnet/
examples/dragnn/interactive_text_analyzer.ipynb

For trainning: 
https://github.com/tensorflow/models/blob/master/syntaxnet/
examples/dragnn/trainer_tutorial.ipynb

"""

import os
import tensorflow as tf
from dragnn.protos import spec_pb2
from dragnn.python import graph_builder
# noinspection PyUnresolvedReferences
from dragnn.python import load_dragnn_cc_impl  # This loads the actual op definitions
from dragnn.python import spec_builder
from google.protobuf import text_format
# noinspection PyUnresolvedReferences
from syntaxnet import load_parser_ops  # This loads the actual op definitions
from syntaxnet import sentence_pb2
from syntaxnet.ops import gen_parser_ops
from tensorflow.python.platform import tf_logging as logging


def load_model(base_dir, master_spec_name, checkpoint_name):
    # Read the master spec
    master_spec = spec_pb2.MasterSpec()
    with open(os.path.join(base_dir, master_spec_name), "r") as f:
        text_format.Merge(f.read(), master_spec)
    spec_builder.complete_master_spec(master_spec, None, base_dir)
    logging.set_verbosity(logging.WARN)  # Turn off TensorFlow spam.

    # Initialize a graph
    graph = tf.Graph()
    with graph.as_default():
        hyperparam_config = spec_pb2.GridPoint()
        builder = graph_builder.MasterBuilder(master_spec, hyperparam_config)
        # This is the component that will annotate input sentences.
        annotator = builder.add_annotation(enable_tracing=True)
        builder.add_saver()  # "Savers" can save and load models; here, we're only going to load.

    sess = tf.Session(graph=graph)
    with graph.as_default():
        # sess.run(tf.global_variables_initializer())
        # sess.run('save/restore_all', {'save/Const:0': os.path.join(base_dir, checkpoint_name)})
        builder.saver.restore(sess, os.path.join(base_dir, checkpoint_name))

    def sent_annotator(sentence):
        with graph.as_default():
            return sess.run([annotator['annotations'], annotator['traces']],
                            feed_dict={annotator['input_batch']: [sentence]})

    return sent_annotator


def annotate(segmenter_model, parser_model, text):
    sentence = sentence_pb2.Sentence(
        text=text,
        token=[sentence_pb2.Token(word=text, start=-1, end=-1)]
    )

    # preprocess
    with tf.Session(graph=tf.Graph()) as tmp_session:
        char_input = gen_parser_ops.char_token_generator([sentence.SerializeToString()])
        preprocessed = tmp_session.run(char_input)[0]
    segmented, _ = segmenter_model(preprocessed)

    annotations, traces = parser_model(segmented[0])
    assert len(annotations) == 1
    assert len(traces) == 1
    dragnn_sent = sentence_pb2.Sentence.FromString(annotations[0])
    dragnn_trace_str = traces[0]
    return dragnn_sent, dragnn_trace_str


def _parse_tree_explorer(dragnn_sent):
    from dragnn.python import render_parse_tree_graphviz

    tree_svg_html = render_parse_tree_graphviz.parse_tree_graph(dragnn_sent)
    html = ('<html>\n'
            '<div style="max-width: 100%%">%s</div>\n'
            '<style type="text/css">svg {{ max-width: 100%%; }}</style>\n'
            '</html>\n') % tree_svg_html  # escaping `%`
    return html


def _trace_explorer(dragnn_trace_str):
    from dragnn.python import visualization

    output = visualization.InteractiveVisualization()
    script_html = output.initial_html()
    trace_html = output.show_trace(dragnn_trace_str)
    html = ('<html>\n'
            '%s\n'
            '%s\n'
            '</html>') % (script_html, trace_html)
    return html


def _browse_html(html, temp_filename='temp.html'):
    import codecs
    import webbrowser

    path = '/tmp/%s' % temp_filename
    url = 'file://' + path
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    webbrowser.open(url)


def _tagged_tuple(token, lookup_dict):
    tag_dict = lookup_dict[token.start]['tag']
    if 'fPOS' in tag_dict:
        ctag, pos = tag_dict['fPOS'].split('++')
    else:
        ctag = 'O'
    token_tuple = [token.word,  # word
                   pos,  # tag
                   ctag,  # ctag
                   '|'.join(['%s=%s' % (k, v) for k, v in tag_dict.items()]),  # feats
                   token.break_level  # break level
                   ]
    return token_tuple


from . import conf

cfg = conf('tensorflow_dragnn_example.conf').get


class TfDragnnNLP(object):
    def __init__(self, lang='en'):
        self._lang = lang
        self.segmenter_model = load_model(cfg(lang, 'seg_dir'),
                                          cfg(lang, 'seg_master_spec_name'),
                                          cfg(lang, 'seg_checkpoint_name'))
        self.parser_model = load_model(cfg(lang, 'parser_dir'),
                                       cfg(lang, 'parser_master_spec_name'),
                                       cfg(lang, 'parser_checkpoint_name'))

    def annotate(self, text):
        dragnn_sent, dragnn_trace_str = annotate(self.segmenter_model, self.parser_model, text)
        return dragnn_sent, dragnn_trace_str

    def tag(self, text):
        dragnn_sent, _ = self.annotate(text)
        parsed_sent = ParsedSent(dragnn_sent)
        return parsed_sent.tagged_list

    def parse(self, text):
        dragnn_sent, _ = self.annotate(text)
        return ParsedSent(dragnn_sent)


from interface import DependencyGraphI
import re

_attr_regex = re.compile('name: "(.*?)" value: "(.*?)"')


class ParsedSent(DependencyGraphI):
    def __init__(self, dragnn_sent):
        super(self.__class__, self).__init__(make_leaf=self._leaf_func)
        # raw result
        self.dragnn_sent = dragnn_sent
        self._lookup_dict, node_num = self.comprehend_dragnn_sent(dragnn_sent)
        # tokens
        self.tagged_list = self._build_tagged_list(node_num)
        # dependency graph
        self.dep_graph, self.root_index = self._build_dep_graph(node_num)

    @classmethod
    def comprehend_dragnn_sent(cls, dragnn_sent):
        token_counter = 0
        # docid = dragnn_sent['docid']
        # text= dragnn_sent['text']
        lookup_dict = dict()
        for token in dragnn_sent.token:
            token_counter += 1
            # word = token.word
            char_pos_start = token.start
            # char_pos_end = token.end
            # char_pos_head = token.head
            attr_list_str = token.tag
            tag_dict = {match.group(1): match.group(2)
                        for match in _attr_regex.finditer(attr_list_str)}
            # category = token.category
            # label = token.label
            # break_level = token.break_level  # enum type of syntaxnet.Token.BreakLevel
            lookup_dict[char_pos_start] = dict()
            # lookup_dict[char_pos_start]['word'] = word
            lookup_dict[char_pos_start]['tag'] = tag_dict
        return lookup_dict, token_counter

    def _build_tagged_list(self, node_num):
        token_list = [[] for _ in range(node_num)]
        for index, token in enumerate(self.dragnn_sent.token):
            token_list[index] = _tagged_tuple(token, self._lookup_dict)
        return token_list

    def _build_dep_graph(self, node_num):
        # dependency graph
        self._dep_graph = [dict() for _ in range(node_num)]
        for index, token in enumerate(self.dragnn_sent.token):
            dep_index = index
            dep_rel = token.label
            head_index = token.head if token.head != -1 else dep_index
            self._add_dep_arc(dep_index, dep_rel, head_index)
        return self._dep_graph, self._root_index

    def _leaf_func(self, index):
        token = self.tagged_list[index]
        # noinspection PyCompatibility
        return '/'.join([token[0], token[1]]).replace('(', u'（').replace('(', u'）')
