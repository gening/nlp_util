# coding: utf-8

"""
Utility Tools for Stanford CoreNLP Server
=========================================
https://stanfordnlp.github.io/CoreNLP/

Stanford CoreNLP – Core natural language software
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

import sys

import os

from pycorenlp import StanfordCoreNLP


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
        self._stanford_nlp = StanfordCoreNLP(server_url)

    def __enter__(self):
        self.set_up(self._lang)
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tear_down()

    @classmethod
    def set_up(cls, lang):
        # start service
        os.system(os.path.join(os.path.dirname(__file__),
                               'stanford_corenlp_server_start.sh %s' % lang))

    @classmethod
    def tear_down(cls):
        # stop service
        os.system(os.path.join(os.path.dirname(__file__),
                               'stanford_corenlp_server_stop.sh'))

    def kernel(self, doc, parsing=True):
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
            conf = 'tokenize, ssplit, pos, lemma, ner, depparse'
            # Note:
            # `coref` must be used with `parse` together for Chinese
            # `dcoref` here does not work for Chinese
            # e.g.
            # conf = ('tokenize, ssplit, pos, lemma, ner, depparse, '
            #         'parse, coref')  # cause timeout
        else:
            conf = 'tokenize, ssplit, pos, lemma, ner'

        # call stanford corenlp server
        corenlp_doc = self._stanford_nlp.annotate(doc, properties={
            'annotators': conf,
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
        corenlp_doc = self.kernel(doc, parsing=False)
        for parsed_sent in corenlp_doc['sentences']:
            tagged_list = [_tagged_tuple(t) for t in parsed_sent['tokens']]
            yield tagged_list

    def parse_with_ssplit(self, doc):
        corenlp_doc = self.kernel(doc, parsing=True)
        if isinstance(corenlp_doc, dict):
            for corenlp_sent in corenlp_doc['sentences']:
                yield ParsedSent(corenlp_sent)
        else:
            # parsing has failed, and corenlp_doc is the error message.
            sys.stderr.write(corenlp_doc)


from interface import SentDependencyI


class ParsedSent(SentDependencyI):
    # parse
    # print(corenlp_doc['sentences'][0]['parse'])
    # from nltk.tree import Tree
    #
    # sent_tree = Tree.fromstring(corenlp_doc['sentences'][0]['kernel'])
    # sent_tree.draw()
    def __init__(self, corenlp_sent):
        self.corenlp_sent = corenlp_sent
        # tokens
        self.tagged_list = self._set_tagged_list()
        # dependency graph
        node_num = len(self.tagged_list)
        self.dep_graph, self.root_index = self._set_dep_graph(node_num)
        super(self.__class__, self).__init__(self.dep_graph, self.root_index,
                                             make_leaf=self._leaf_func)

    def _set_tagged_list(self):
        # dependency vertices
        # tokens
        tagged_list = [_tagged_tuple(t) for t in self.corenlp_sent['tokens']]
        return tagged_list

    def _set_dep_graph(self, node_num):
        # dependency arcs
        # basicDependencies, enhancedDependencies, enhancedPlusPlusDependencies
        corenlp_dep = self.corenlp_sent['enhancedPlusPlusDependencies']

        # dependency graph
        # root: of the first tree
        root_id = None
        # arcs: from tail to head
        dep_graph = [dict() for _ in range(node_num)]
        # arcs: from head to tail
        for d in corenlp_dep:
            dep_id = d['dependent'] - 1
            dep_rel = d['dep']
            head_id = d['governor'] - 1

            # option `enhancedPlusPlusDependencies` may cause one mapped to two heads.
            # these relations are stored in the dep_graph[head_id]['deps']
            # dep_graph[dep_id]['head'] is only the nearest head_id.
            if ('head' not in dep_graph[dep_id] or (
                            dep_graph[dep_id]['head'] != -1 and (
                                abs(head_id - dep_id) < abs(dep_graph[dep_id]['head'] - dep_id)))):
                dep_graph[dep_id]['rel'] = dep_rel
                dep_graph[dep_id]['head'] = head_id

            if head_id == -1:  # head_id = -1
                if root_id is None:
                    root_id = dep_id
                else:
                    root_id = min(dep_id, root_id)
            else:
                dep_graph[head_id].setdefault(
                    'deps', dict()).setdefault(
                    dep_rel, list()).append(dep_id)

        return dep_graph, root_id

    def _leaf_func(self, index):
        token = self.tagged_list[index]
        # noinspection PyCompatibility
        return '/'.join([token[0], token[1]]).replace('(', u'（').replace('(', u'）')
