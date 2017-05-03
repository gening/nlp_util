# coding: utf-8

"""
Utility Tools for Stanford NLP
==============================
# The NLTK wrapper of stanford nlp postagger, ner and parser,
# working much slower than the Standford Corenlp Server.
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

import sys

if sys.version_info[0] == 2:  # python 2
    # noinspection PyCompatibility,PyUnresolvedReferences
    from ConfigParser import ConfigParser
elif sys.version_info[0] == 3:  # python 3
    # noinspection PyCompatibility,PyUnresolvedReferences
    from configparser import ConfigParser

conf = ConfigParser()

import codecs

with codecs.open('stanford_nltk_nlp.conf', 'r', encoding='utf-8') as f:
    conf.readfp(f)
cfg = conf.get
stanford_nlp_dir = cfg('base', 'dir')


class StanfordNLP(object):
    def __init__(self, lang='en', parse=True):
        if lang in ['en', 'zh']:
            self._lang = lang
        else:
            raise ValueError('not supported %s language' % lang)
        self.stanford_tokenizer = None
        self.stanford_pos = None
        self.stanford_ner = None
        self.stanford_parser = None

    def setup_tag(self):
        from nltk.tokenize.stanford import StanfordTokenizer
        path_to_jar = stanford_nlp_dir + '/' + cfg('pos', 'path_jar') + '/' + cfg('pos', 'name_jar')
        self.stanford_tokenizer = StanfordTokenizer(path_to_jar)

        from nltk.tag.stanford import StanfordPOSTagger
        path_to_jar = stanford_nlp_dir + '/' + cfg('pos', 'path_jar') + '/' + cfg('pos', 'name_jar')
        model_filename = (stanford_nlp_dir + '/' + cfg('pos', 'path_model') + '/' +
                          cfg(self._lang, 'pos_model'))
        self.stanford_pos = StanfordPOSTagger(model_filename, path_to_jar)

        from nltk.tag.stanford import StanfordNERTagger
        path_to_jar = stanford_nlp_dir + '/' + cfg('ner', 'path_jar') + '/' + cfg('ner', 'name_jar')
        model_filename = (stanford_nlp_dir + '/' + cfg('ner', 'path_model') + '/' +
                          cfg(self._lang, 'ner_model'))
        self.stanford_ner = StanfordNERTagger(model_filename, path_to_jar)

    def setup_parser(self):
        # from nltk.parse.stanford import StanfordParser

        # path_to_jar = (stanford_nlp_dir + '/' + cfg('parser','path_jar') + '/' + 
        #                cfg('parser','name_jar'))
        # path_to_models_jar = (stanford_nlp_dir + '/' + cfg('parser','path_model_jar') + '/' + 
        #                       cfg('parser','name_model_jar'))
        # model_path = cfg('parser', 'model_path') + '/' + cfg(self._lang, 'parser_model')
        # self.stanford_parser = StanfordParser(path_to_jar, path_to_models_jar, model_path)
        # print(list(stanford_parser.raw_parse(text)))
        # for sent_tree in stanford_parser.raw_parse(text):
        #     sent_tree.draw()

        from nltk.parse.stanford import StanfordDependencyParser
        path_to_jar = (stanford_nlp_dir + '/' + cfg('parser', 'path_jar') + '/' +
                       cfg('parser', 'name_jar'))
        path_to_models_jar = (stanford_nlp_dir + '/' + cfg('parser', 'path_model_jar') + '/' +
                              cfg('parser', 'name_model_jar'))
        model_path = cfg('parser', 'model_path') + '/' + cfg(self._lang, 'parser_model')
        self.stanford_parser = StanfordDependencyParser(path_to_jar, path_to_models_jar, model_path)
        # for dep_graph in stanford_parser.raw_parse(text):
        #     print dep_graph
        #     dep_graph.tree().draw()

    def tag(self, text):
        """
        
        :param text: 
        :return: 
        """
        word_list = self.stanford_tokenizer.tokenize(text)
        word_pos_list = self.stanford_pos.tag(word_list)
        word_ner_list = self.stanford_ner.tag(word_list)
        word_pos_ner_list = zip(word_list, zip(*word_pos_list)[1], zip(*word_ner_list)[1])
        return word_pos_ner_list

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
