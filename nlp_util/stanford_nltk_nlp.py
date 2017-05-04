# coding: utf-8

"""
Utility Tools for Stanford NLP
==============================
The NLTK wrapper of stanford nlp postagger, ner and parser

Each calling of functions will evoke an entirely new shell command of java, 
so these interfaces are much slower than Standford Corenlp Server.
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

import sys

import codecs
from os import path

if sys.version_info[0] == 2:  # python 2
    # noinspection PyCompatibility,PyUnresolvedReferences
    from ConfigParser import ConfigParser
elif sys.version_info[0] == 3:  # python 3
    # noinspection PyCompatibility,PyUnresolvedReferences
    from configparser import ConfigParser

conf = ConfigParser()

with codecs.open(path.join(path.dirname(__file__), 'stanford_nltk_nlp.conf'),
                 'r', encoding='utf-8') as f:
    conf.readfp(f)
cfg = conf.get


def set_up_seg(lang):
    if lang in ['zh', 'ar']:
        from nltk.tokenize.stanford_segmenter import StanfordSegmenter
        path_to_jar = path.join(cfg('seg', 'path'), cfg('seg', 'path_jar'))
        path_to_slf4j = path_to_jar  # slf4j cannot be found any more in v3.7
        path_to_sihan_corpora_dict = path.join(cfg('seg', 'path'), cfg('seg', 'path_data'))
        path_to_model = path.join(cfg('seg', 'path'), cfg('seg', 'path_data'),
                                  cfg(lang, 'seg_model'))
        path_to_dict = path.join(cfg('seg', 'path'), cfg('seg', 'path_data'),
                                 cfg(lang, 'seg_dict'))
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
        stanford_tokenize_func = (lambda text: stanford_segmenter.segment(text).split())
    else:  # if lang in ['en', 'fr', 'es']:
        from nltk.tokenize.stanford import StanfordTokenizer
        path_to_jar = path.join(cfg('pos', 'path'), cfg('pos', 'path_jar'))
        stanford_tokenize_func = StanfordTokenizer(path_to_jar).tokenize
    return stanford_tokenize_func


def set_up_pos_tag(lang):
    from nltk.tag.stanford import StanfordPOSTagger
    path_to_jar = path.join(cfg('pos', 'path'), cfg('pos', 'path_jar'))
    model_filename = path.join(cfg('pos', 'path'), cfg('pos', 'path_model'),
                               cfg(lang, 'pos_model'))
    stanford_postagger = StanfordPOSTagger(model_filename, path_to_jar)
    if lang in ['zh']:
        # [('', u'中文#NN'), ...]
        stanford_pos_func = (lambda word_list:
                             [t[1].split('#') for t in stanford_postagger.tag(word_list)])
    else:
        stanford_pos_func = stanford_postagger.tag
    return stanford_pos_func


def set_up_ner_tag(lang):
    from nltk.tag.stanford import StanfordNERTagger
    path_to_jar = path.join(cfg('ner', 'path'), cfg('ner', 'path_jar'))
    model_filename = path.join(cfg('ner', 'path'), cfg('ner', 'path_model'),
                               cfg(lang, 'ner_model'))
    stanford_ner_func = StanfordNERTagger(model_filename, path_to_jar).tag
    return stanford_ner_func


def set_up_parse(lang):
    # from nltk.kernel.stanford import StanfordParser

    # path_to_jar = path.join(cfg('parser', 'path'), cfg('parser', 'path_jar'))
    # path_to_models_jar = path.join(cfg('parser', 'path'), cfg('parser', 'path_model_jar'))
    # model_path = path.join(cfg('parser', 'model_path'), cfg(self._lang, 'parser_model'))
    # self.stanford_parser = StanfordParser(path_to_jar, path_to_models_jar, model_path)
    # print(list(stanford_parser.raw_parse(text)))
    # for sent_tree in stanford_parser.raw_parse(text):
    #     sent_tree.draw()

    from nltk.parse.stanford import StanfordDependencyParser
    path_to_jar = path.join(cfg('parser', 'path'), cfg('parser', 'path_jar'))
    path_to_models_jar = path.join(cfg('parser', 'path'), cfg('parser', 'path_model_jar'))
    model_path = path.join(cfg('parser', 'model_path'), cfg(lang, 'parser_model'))
    stanford_parser = StanfordDependencyParser(path_to_jar, path_to_models_jar, model_path)
    # for dep_graph in stanford_parser.raw_parse(text):
    #     print dep_graph
    #     dep_graph.tree().draw()
    return stanford_parser


class StanfordNLP(object):
    def __init__(self, lang='en'):
        if lang not in ['en', 'zh']:
            raise ValueError('not supported `%s` language' % lang)
        self._lang = lang
        self.stanford_token_seg = None
        self.stanford_pos_tag = None
        self.stanford_ner_tag = None
        self.stanford_parse = None

    def set_up_tag_func(self):
        if self.stanford_token_seg is None:
            self.stanford_token_seg = set_up_seg(self._lang)
        if self.stanford_pos_tag is None:
            self.stanford_pos_tag = set_up_pos_tag(self._lang)
        if self.stanford_ner_tag is None:
            self.stanford_ner_tag = set_up_ner_tag(self._lang)
        if self.stanford_parse is None:
            self.stanford_parse = set_up_parse(self._lang)

    def set_up_parse_func(self):
        if self.stanford_token_seg is None:
            self.stanford_token_seg = set_up_seg(self._lang)
        if self.stanford_parse is None:
            self.stanford_parse = set_up_parse(self._lang)

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

    def parse(self):
        self.set_up_parse_func()
        pass

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
# from nltk.kernel.stanford import StanfordDependencyParser
#
# stanford_parser = StanfordDependencyParser()
# print [list(kernel.triples()) for kernel in stanford_parser.raw_parse(text)]
