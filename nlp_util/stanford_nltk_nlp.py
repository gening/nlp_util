# coding: utf-8

"""
Utility Tools for Stanford NLP
==============================
The NLTK wrapper of stanford nlp postagger, ner and parser

Each calling of functions will evoke an entirely new shell command of java and its initialization, 
so these interfaces are much slower than Standford Corenlp Server, which is initialized only once.
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

from . import conf

cfg = conf('stanford_nlp.conf').get


def get_seg(lang):
    if lang in ['zh', 'ar']:
        from nltk.tokenize.stanford_segmenter import StanfordSegmenter
        path_to_jar = cfg('seg', 'jar')
        path_to_slf4j = path_to_jar  # slf4j cannot be found any more in v3.7
        path_to_sihan_corpora_dict = cfg('seg', 'path_data')
        path_to_model = cfg('seg', 'model_' + lang)
        path_to_dict = cfg('seg', 'dict_' + lang)
        # path_to_jar = "stanford-segmenter-3.6.0.jar",
        # path_to_slf4j = "slf4j-api.jar",
        # path_to_sihan_corpora_dict = "./data",
        # path_to_model = "./data/pku.gz",
        # path_to_dict = "./data/dict-chris6.ser.gz"
        stanford_segmenter = StanfordSegmenter(path_to_jar,
                                               path_to_slf4j,
                                               path_to_sihan_corpora_dict,
                                               path_to_model,
                                               path_to_dict)
        # not support sent split
        stanford_tokenize_func = (lambda text: stanford_segmenter.segment(text).split())
    else:  # if lang in ['en', 'fr', 'es']:
        from nltk.tokenize.stanford import StanfordTokenizer
        path_to_jar = cfg('pos', 'jar')
        # cannot call tokenize_sents() because it support sent_list but not support sent split
        stanford_tokenize_func = StanfordTokenizer(path_to_jar).tokenize
    return stanford_tokenize_func


def get_pos_tag(lang):
    from nltk.tag.stanford import StanfordPOSTagger
    path_to_jar = cfg('pos', 'jar')
    model_filename = cfg('pos', 'model_' + lang)
    stanford_postagger = StanfordPOSTagger(model_filename, path_to_jar)
    if lang in ['zh']:
        # [('', u'中文#NN'), ...]
        stanford_pos_func = (lambda word_list:
                             [t[1].split('#') for t in stanford_postagger.tag(word_list)])
    else:
        stanford_pos_func = stanford_postagger.tag
    return stanford_pos_func


def get_ner_tag(lang):
    from nltk.tag.stanford import StanfordNERTagger
    path_to_jar = cfg('ner', 'jar')
    model_filename = cfg('ner', 'model_' + lang)
    stanford_ner_func = StanfordNERTagger(model_filename, path_to_jar).tag
    return stanford_ner_func


def get_syntactic_parser(lang):
    from nltk.parse.stanford import StanfordParser

    path_to_jar = cfg('parser', 'jar')
    path_to_models_jar = cfg('parser', 'model_jar')
    model_path = cfg('parser', 'model_' + lang)
    stanford_parser = StanfordParser(path_to_jar, path_to_models_jar, model_path)
    # print(list(stanford_dep_parser.raw_parse(text)))
    # for sent_tree in stanford_dep_parser.raw_parse(text):
    #     sent_tree.draw()
    return stanford_parser


def get_dep_parser(lang):
    # statical dependency parser
    from nltk.parse.stanford import StanfordDependencyParser
    path_to_jar = cfg('parser', 'jar')
    path_to_models_jar = cfg('parser', 'model_jar')
    model_path = cfg('parser', 'model_' + lang)
    stanford_dep_parser = StanfordDependencyParser(path_to_jar, path_to_models_jar, model_path)
    return stanford_dep_parser


def get_nndep_parser(lang):
    # neural network dependency parser
    from nltk.parse.stanford import StanfordNeuralDependencyParser
    path_to_jar = cfg('corenlp', 'jar')
    path_to_models_jar = cfg('corenlp_model', 'jar_' + lang)
    model_path = cfg('nndep', 'model_' + lang)
    stanford_nndep_parser = StanfordNeuralDependencyParser(path_to_jar, path_to_models_jar,
                                                           model_path)
    # set to 2-4GB, otherwise default `-mx1000m` causes java.lang.OutOfMemoryError
    stanford_nndep_parser.java_options = '-mx4g'
    return stanford_nndep_parser


class StanfordNLP(object):
    def __init__(self, lang='en'):
        if lang not in ['en', 'zh']:
            raise ValueError('not supported `%s` language' % lang)
        self._lang = lang
        self.stanford_token_seg = None
        self.stanford_pos_tag = None
        self.stanford_ner_tag = None
        self.stanford_parser = None
        self.stanford_dep_parser = None
        self.stanford_nndep_parser = None

    def set_up_tag_func(self):
        if self.stanford_token_seg is None:
            self.stanford_token_seg = get_seg(self._lang)
        if self.stanford_pos_tag is None:
            self.stanford_pos_tag = get_pos_tag(self._lang)
        if self.stanford_ner_tag is None:
            self.stanford_ner_tag = get_ner_tag(self._lang)

    def set_up_dep_parser(self):
        if self.stanford_token_seg is None:
            self.stanford_token_seg = get_seg(self._lang)
        if self.stanford_pos_tag is None:
            self.stanford_pos_tag = get_pos_tag(self._lang)
        if self.stanford_ner_tag is None:
            self.stanford_ner_tag = get_ner_tag(self._lang)
        if self.stanford_dep_parser is None:
            self.stanford_dep_parser = get_dep_parser(self._lang)

    def set_up_nndep_parser(self):
        if self.stanford_ner_tag is None:
            self.stanford_ner_tag = get_ner_tag(self._lang)
        if self.stanford_nndep_parser is None:
            self.stanford_nndep_parser = get_nndep_parser(self._lang)

    def tag(self, text):
        """
        
        :param text: 
        :return: yield [(word, pos ,ner), ...] of a sentence
        """
        self.set_up_tag_func()
        word_list = self.stanford_token_seg(text)
        word_pos_list = self.stanford_pos_tag(word_list)
        word_ner_list = self.stanford_ner_tag(word_list)
        word_pos_ner_list = zip(word_list, zip(*word_pos_list)[1], zip(*word_ner_list)[1])
        return word_pos_ner_list

    def parse(self, text):
        # does not support sent split
        self.set_up_dep_parser()
        word_list = self.stanford_token_seg(text)
        word_pos_list = self.stanford_pos_tag(word_list)
        word_ner_list = self.stanford_ner_tag(word_list)
        word_pos_ner_list = zip(word_list, zip(*word_pos_list)[1], zip(*word_ner_list)[1])
        nltk_dep_graph_list = self.stanford_dep_parser.tagged_parse(word_pos_list)
        # !important: all punctuations will be swallowed by StanfordDependencyParser
        for nltk_dep_graph in nltk_dep_graph_list:
            # only return the first dependency graph in the result.
            return ParsedSent(nltk_dep_graph, word_pos_ner_list)

    def parse_with_ssplit(self, doc):
        # support sent split
        if self._lang in ['zh']:
            raise NotImplementedError('Because tagged_parse() is not supported by '
                                      'nltk.parse.stanford.StanfordNeuralDependencyParser, '
                                      'use parse() instead, which based on '
                                      'nltk.parse.stanford.StanfordDependencyParser.')
        self.set_up_nndep_parser()
        # stanford_dep_parser.raw_parse() can process English with tokenizing and sent splitting,
        # but does not support Chinese segment.
        nltk_dep_graph_list = self.stanford_nndep_parser.raw_parse(doc.replace('\n', ''))
        for nltk_dep_graph in nltk_dep_graph_list:
            parsed_sent = ParsedSent(nltk_dep_graph)
            # tag ner after parsing
            tagged_list = parsed_sent.tagged_list
            word_list = zip(*tagged_list)[0]
            word_ner_list = self.stanford_ner_tag(word_list)
            # insert into tagged_list
            for i in range(len(tagged_list)):
                tagged_tuple = list(tagged_list[i])
                tagged_tuple.insert(2, word_ner_list[i][1])
                tagged_list[i] = tagged_tuple
            # ner tagged
            yield parsed_sent


# CoNLL-U Format
# http://universaldependencies.org/format.html
# conll-U = "word \t tag \t head \n word \t tag \t head \n ... \n\n ..."
# CoNLL-3: word, tag, head
# CoNLL-4: word, tag, head, rel
# CoNLL-10: id, word, lemma, ctag, tag, feats, head, rel, deps, misc
# id = 1 - based inline index
# 1 They  they PRON  PRP Case=Nom|Number=Plur            2 nsubj 2:nsubj|4:nsubj  _
# 2 buy   buy  VERB  VBP Number=Plur|Person=3|Tense=Pres 0 root  0:root           _
# 3 and   and  CONJ  CC  _                               4 cc    4:cc             _
# 4 sell  sell VERB  VBP Number=Plur|Person=3|Tense=Pres 2 conj  0:root|2:conj    _
# 5 books book NOUN  NNS Number=Plur                     2 obj   2:obj|4:obj      SpaceAfter=No
# 6 .     .    PUNCT .   _                               2 punct 2:punct          _
def _tagged_tuple(token):
    token_tuple = [token[1],  # word
                   token[4],  # tag
                   # token[3],  # ctag == tag
                   # token[5],  # feats == ''
                   token[1] if token[2] == '_' else token[2]  # lemma
                   ]
    return token_tuple


from interface import DependencyGraphI


class ParsedSent(DependencyGraphI):
    def __init__(self, nltk_dependency_graph, word_pos_ner_list=None):
        super(self.__class__, self).__init__(make_leaf=self._leaf_func)
        # raw result
        self.nltk_dependency_graph = nltk_dependency_graph
        # tokens
        if word_pos_ner_list:
            self.tagged_list = word_pos_ner_list
        else:
            self.tagged_list = self._build_tagged_list()
        # dependency graph
        node_num = len(self.tagged_list)
        self.dep_graph, self.root_index = self._build_dep_graph(node_num)

    def _build_tagged_list(self):
        return map(_tagged_tuple,
                   [token.split('\t') for token
                    in self.nltk_dependency_graph.to_conll(10).split('\n') if token != ''])

    def _build_dep_graph(self, node_num):
        # change dep_graph_nodes from 1-based to 0-based
        dep_graph_nodes = self.nltk_dependency_graph.nodes
        dep_graph = [dict() for _ in range(node_num)]
        for token in dep_graph_nodes.values():
            index = token['address'] - 1
            if index == -1:
                continue
            dep_graph[index]['rel'] = token['rel']
            dep_graph[index]['head'] = token['head'] - 1 if token['head'] - 1 != -1 else index
            if token['deps']:
                # dep_graph[index]['deps'] = {dep_rel: map(lambda x: x - 1, dep_id_list)
                #                             for dep_rel, dep_id_list in token['deps'].items()}
                dep_graph[index]['deps'] = dict()
                for dep_rel, dep_id_list in token['deps'].items():
                    dep_graph[index]['deps'][dep_rel] = map(lambda x: x - 1, dep_id_list)
        root_index = self.nltk_dependency_graph.root['address'] - 1
        if root_index == -1:
            root_index = None
        return dep_graph, root_index

    def _leaf_func(self, index):
        token = self.nltk_dependency_graph.get_by_address(index + 1)
        return '/'.join([token['word'], token['tag']])

# for reference
#
# import os
#
# stanford_nlp_dir = '/Volumes/Documents/Projects/~stanford_nlp'
# stanford_nlp_class = [os.environ.get('CLASSPATH', '')]
# stanford_nlp_models = [os.environ.get('STANFORD_MODELS', '')]
#
# # Add the directories containing stanford-postagger.jar, stanford-ner.jar and stanford-parser.jar
# # to the CLASSPATH environment variable
#
# stanford_nlp_class.append(os.path.join(stanford_nlp_dir, 'stanford-postagger-full-2016-10-31'))
# stanford_nlp_class.append(os.path.join(stanford_nlp_dir, 'stanford-ner-2016-10-31'))
# stanford_nlp_class.append(os.path.join(stanford_nlp_dir, 'stanford-parser-full-2016-10-31'))
# os.environ['CLASSPATH'] = ':'.join(stanford_nlp_class)
#
# # Point the STANFORD_MODELS environment variable to the directory containing
# # the stanford tokenizer models, stanford pos models, stanford ner models, stanford parser models
# # e.g. arabic.tagger, arabic-train.tagger, chinese-distsim.tagger,stanford-parser-x.x.x-models.jar
# # e.g. export STANFORD_MODELS=/usr/share/stanford-postagger-full-2015-01-30/models:/usr/share/
# # stanford-ner-2015-04-20/classifier
#
# stanford_nlp_models.append(os.path.join(stanford_nlp_dir,
#                                         'stanford-postagger-full-2016-10-31', 'models'))
# stanford_nlp_models.append(os.path.join(stanford_nlp_dir,
#                                         'stanford-ner-2016-10-31', 'classifiers'))
# stanford_nlp_models.append(os.path.join(stanford_nlp_dir, 'stanford-parser-full-2016-10-31'))
# os.environ['STANFORD_MODELS'] = ':'.join(stanford_nlp_models)
#
# model_name_pos = 'english-bidirectional-distsim.tagger'
# model_name_ner = 'english.all.3class.distsim.crf.ser.gz'
#
# from nltk.tokenize.stanford import StanfordTokenizer
#
# stanford_tokenizer = StanfordTokenizer()
# word_list = stanford_tokenizer.tokenize(text)
#
# from nltk.tag import StanfordPOSTagger
#
# stanford_pos = StanfordPOSTagger(model_name_pos)
# word_pos_list = stanford_pos.tag(word_list)
#
# from nltk.tag import StanfordNERTagger
#
# stanford_ner = StanfordNERTagger(model_name_ner)
# word_ner_list = stanford_ner.tag(word_list)
#
# from nltk.parse.stanford import StanfordDependencyParser
#
# stanford_parser = StanfordDependencyParser()
# print [list(parse.triples()) for parse in stanford_parser.raw_parse(text)]
