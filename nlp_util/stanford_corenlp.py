# coding: utf-8

"""
Utility Tools for Stanford CoreNLP Server
=========================================
https://stanfordnlp.github.io/CoreNLP/

Stanford CoreNLP – Core natural language software, 
developed by The Natural Language Processing Group at Stanford University, US
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

import sys

import os

import pycorenlp
from . import conf

cfg = conf('stanford_nlp.conf').get


def _tagged_tuple(token):
    # [word, pos, ner, speaker, lemma]
    token_tuple = []
    for key in ['word', 'pos', 'ner', 'lemma']:
        if key in token:
            token_tuple.append(token[key])
    return token_tuple


class StanfordNLP(object):
    def __init__(self, lang='en', server_url='http://localhost:9000'):  # lang = 'zh'
        self._lang = lang
        self._stanford_nlp = pycorenlp.StanfordCoreNLP(server_url)

    def __enter__(self):
        stanford_corenlp_path = cfg('corenlp', 'path_base')
        stanford_corenlp_model_path = cfg('corenlp_model', 'path_base')
        self.set_up(stanford_corenlp_path, stanford_corenlp_model_path, self._lang)
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tear_down()

    @classmethod
    def set_up(cls, stanford_corenlp_path, stanford_corenlp_model_path, lang):
        # start service
        os.system(os.path.join(
            os.path.dirname(__file__),
            'stanford_corenlp_server_start.sh %s %s %s' % (stanford_corenlp_path,
                                                           stanford_corenlp_model_path,
                                                           lang)))

    @classmethod
    def tear_down(cls):
        # stop service
        os.system(os.path.join(os.path.dirname(__file__),
                               'stanford_corenlp_server_stop.sh'))

    def annotate(self, doc, parsing=True):
        # The annotators enabled by default are:
        # -annotators tokenize, ssplit, pos, lemma, ner, depparse, coref, natlog, openie.
        # The default annotators do not include the parse annotator.
        # This is primarily for efficiency.
        #
        # Annotatos:
        # https://stanfordnlp.github.io/CoreNLP/dependencies.html
        # tokenize, ssplit, pos, lemma, ner, # ssplit = sent split
        # depparse, parse, dcoref, coref, mention, entitymentions,
        # sentiment, natlog, openie

        if parsing:
            # Must deparse to load model from edu/stanford/nlp/models/parser/nndep/ for Chinese
            # otherwise dependency parsing Chinese sentences will raise a "no head rule" error.
            annotators = 'tokenize, ssplit, pos, lemma, ner, depparse'
            # Note:
            # `coref` must be used with `parse` together for Chinese
            # `dcoref` here does not work for Chinese
            # e.g.
            # annotators = ('tokenize, ssplit, pos, lemma, ner, depparse, '
            #               'parse, coref')  # cause timeout
        else:
            annotators = 'tokenize, ssplit, pos, lemma, ner'

        # call stanford corenlp server
        corenlp_doc = self._stanford_nlp.annotate(doc, properties={
            'annotators': annotators,
            'outputFormat': 'json'
        })

        # # corenlp_doc
        # print(corenlp_doc['sentences'][0].keys())
        # [u'index', u'tokens',
        #  u'basicDependencies', u'enhancedDependencies', u'enhancedPlusPlusDependencies',
        #  u'parse']
        return corenlp_doc

    def tag_with_ssplit(self, doc):
        # tokens
        # print corenlp_doc['sentences'][0]['tokens'][0].keys()
        # [u'index', u'word', u'lemma', u'originalText', u'pos', u'before', u'after',
        #  u'characterOffsetEnd', u'characterOffsetBegin', u'ner', u'speaker']
        corenlp_doc = self.annotate(doc, parsing=False)
        for parsed_sent in corenlp_doc['sentences']:
            tagged_list = [_tagged_tuple(t) for t in parsed_sent['tokens']]
            yield tagged_list

    def parse_with_ssplit(self, doc):
        corenlp_doc = self.annotate(doc, parsing=True)
        if isinstance(corenlp_doc, dict):
            for corenlp_sent in corenlp_doc['sentences']:
                yield ParsedSent(corenlp_sent)
        else:
            # parsing has failed, and corenlp_doc is the error message.
            sys.stderr.write(corenlp_doc)


from interface import DependencyGraphI


class ParsedSent(DependencyGraphI):
    # parse
    # print(corenlp_doc['sentences'][0]['parse'])
    # from nltk.tree import Tree
    #
    # sent_tree = Tree.fromstring(corenlp_doc['sentences'][0]['parse'])
    # sent_tree.draw()
    def __init__(self, corenlp_sent):
        super(self.__class__, self).__init__(make_leaf=self._leaf_func)
        # raw result
        self.corenlp_sent = corenlp_sent
        # tokens
        self.tagged_list = self._build_tagged_list()
        # dependency graph
        node_num = len(self.tagged_list)
        self.dep_graph, self.root_index = self._build_dep_graph(node_num)

    def _build_tagged_list(self):
        # dependency vertices
        # tokens
        tagged_list = [_tagged_tuple(t) for t in self.corenlp_sent['tokens']]
        return tagged_list

    def _build_dep_graph(self, node_num):
        # dependency arcs
        # basicDependencies, enhancedDependencies, enhancedPlusPlusDependencies
        corenlp_dep = self.corenlp_sent['enhancedPlusPlusDependencies']

        # dependency graph
        root_index = None
        self._dep_graph = [dict() for _ in range(node_num)]
        for d in corenlp_dep:
            dep_index = d['dependent'] - 1
            dep_rel = d['dep']
            head_index = d['governor'] - 1 if d['governor'] - 1 != -1 else dep_index
            # option `enhancedPlusPlusDependencies` may cause one mapped to two heads.
            root_index = self._add_dep_arc(dep_index, dep_rel, head_index)
        return self._dep_graph, root_index

    def _leaf_func(self, index):
        token = self.tagged_list[index]
        # noinspection PyCompatibility
        return '/'.join([token[0], token[1]]).replace('(', u'（').replace('(', u'）')
