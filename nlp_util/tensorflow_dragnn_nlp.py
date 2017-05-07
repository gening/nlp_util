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

data_path = os.path.join(os.path.dirname(__file__), 'data')


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

    def annotate_sentence(sentence):
        with graph.as_default():
            return sess.run([annotator['annotations'], annotator['traces']],
                            feed_dict={annotator['input_batch']: [sentence]})

    return annotate_sentence


segmenter_model = load_model(os.path.join(data_path, "dragnn/en/segmenter"),
                             "spec.textproto", "checkpoint")
parser_model = load_model(os.path.join(data_path, "dragnn/en"),
                          "parser_spec.textproto", "checkpoint")


def annotate(text):
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


def _view_html(html, temp_filename='temp.html'):
    import codecs
    import webbrowser

    path = '/tmp/%s' % temp_filename
    url = 'file://' + path
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    webbrowser.open(url)


import re

regex = re.compile('name: "(.*?)" value: "(.*?)"')


def cast(dragnn_sent):
    # docid = dragnn_sent['docid']
    # text= dragnn_sent['text']
    tagged_list = []
    for token in dragnn_sent.token:
        word = token.word
        char_start = token.start
        char_end = token.end
        char_head = token.head
        attr_list_str = token.tag
        tags = {match.group(1): match.group(2)
                for match in regex.finditer(attr_list_str)}
        category = token.category
        label = token.label
        break_level = token.break_level  # enum type of syntaxnet.Token.BreakLevel
        token_dict = {'word': word,
                      'char_start': char_start, 'char_end': char_end, 'char_head': char_head,
                      'tags': tags,
                      'category': category,
                      'dep': label,
                      'break_level': break_level}
        tagged_list.append(token_dict)
    return tagged_list


def main():
    from pprint import pprint
    dragnn_sent, dragnn_trace_str = annotate("John is eating pizza with a fork")
    # Also try: John is eating pizza with a fork
    pprint(cast(dragnn_sent))
    dependency_tree_html = _parse_tree_explorer(dragnn_sent)
    _view_html(dependency_tree_html, 'temp_dragnn_tree.html')
    neural_graph_html = _trace_explorer(dragnn_trace_str)
    _view_html(neural_graph_html, 'temp_dragnn_graph.html')


if __name__ == '__main__':
    main()
