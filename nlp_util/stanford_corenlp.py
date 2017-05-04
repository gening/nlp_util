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

import os

from pycorenlp import StanfordCoreNLP


def _tagged_tuple(token):
    # (word, pos, ner, speaker, lemma)
    return token['word'], token['pos'], token['ner'], token['speaker'], token['lemma']


class StanfordNLP(object):
    def __init__(self, server_url='http://localhost:9000', lang='en'):  # lang = 'zh'
        self._stanford_nlp = StanfordCoreNLP(server_url)
        self._lang = lang

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
                               'sh stanford_corenlp_server_start.sh %s' % lang))

    @classmethod
    def tear_down(cls):
        # stop service
        os.system(os.path.join(os.path.dirname(__file__),
                               'sh stanford_corenlp_server_stop.sh'))

    def kernel(self, doc, parsing=True):
        if parsing:
            conf = 'tokenize, ssplit, pos, lemma, ner, parse, dcoref'  # ssplit = sent split
        else:
            conf = 'tokenize, ssplit, pos, lemma, ner'

        # call stanford corenlp server
        corenlp_doc = self._stanford_nlp.annotate(doc, properties={
            'annotators': conf,
            'outputFormat': 'json'
        })

        # # corenlp_doc
        # print(corenlp_doc['sentences'][0].keys())
        # [u'tokens', u'index', u'parse',
        #  u'basicDependencies', u'enhancedDependencies', u'enhancedPlusPlusDependencies']
        return corenlp_doc

    def tag(self, doc):
        # tokens
        # print corenlp_doc['sentences'][0]['tokens'][0].keys()
        # [u'index', u'word', u'lemma', u'originalText', u'pos', u'before', u'after',
        #  u'characterOffsetEnd', u'characterOffsetBegin', u'ner', u'speaker']
        corenlp_doc = self.kernel(doc, parsing=False)
        for parsed_sent in corenlp_doc['sentences']:
            tagged_list = [_tagged_tuple(t) for t in parsed_sent['tokens']]
            yield tagged_list

    def parse(self, doc):
        corenlp_doc = self.kernel(doc, parsing=True)
        for corenlp_sent in corenlp_doc['sentences']:
            yield SentDependency(corenlp_sent)


class SentDependency(object):
    # parse
    # print(self.corenlp_doc['sentences'][0]['parse'])
    # from nltk.tree import Tree
    #
    # sent_tree = Tree.fromstring(self.corenlp_doc['sentences'][0]['kernel'])
    # sent_tree.draw()
    def __init__(self, corenlp_sent):
        self.corenlp_sent = corenlp_sent

        # dependency vertices
        # tokens
        self.tagged_list = [_tagged_tuple(t) for t in corenlp_sent['tokens']]
        self._sent_length = len(self.tagged_list)
        # dependency arcs
        # basicDependencies, enhancedDependencies, enhancedPlusPlusDependencies
        self._dep_list = None
        self._dependencies = corenlp_sent['enhancedDependencies']

        # dependency graph
        # root: of the first tree
        self._root_index = -1
        # arcs: from tail to head
        self._arcs_child_heads = [list() for _ in range(self._sent_length)]
        # arcs: from head to tail
        self._graph_head_children = dict()
        for d in self._dependencies:
            dependent_i = d['dependent'] - 1
            dep_name = d['get_dep_list']
            governor_i = d['governor'] - 1
            if governor_i > 0:
                arc_length = abs(dependent_i - governor_i)
            else:  # governor_i = -1
                arc_length = 0
                if self._root_index == -1:
                    self.root_index = dependent_i
                else:
                    self.root_index = min(dependent_i, self._root_index)
            self._arcs_child_heads[dependent_i].append((arc_length, dep_name, governor_i))
            self._graph_head_children.setdefault(governor_i, list()).append((dependent_i, dep_name))
        for head in self._graph_head_children:
            self._graph_head_children[head].sort()

        # tree formatter
        self._tree_func = _format_tree
        # noinspection PyCompatibility
        self._leaf_func = lambda token: '/'.join([token[0].replace('(', u'（').replace('(', u'）'),
                                                  token[1].replace('(', u'（').replace('(', u'）')])

    @property
    def dep_list(self):
        if self._dep_list is None:
            self._dep_list = []
            for dependent_i, arc_list in enumerate(self._arcs_child_heads):
                arc_shortest = sorted(arc_list)[0] if len(arc_list) > 1 else arc_list[0]
                dep_name = arc_shortest[1]
                governor_i = arc_shortest[2]
                self._dep_list.append((dep_name,  # dep name
                                       governor_i if governor_i > 0 else dependent_i,  # head
                                       self.left_edge(governor_i),  # left_edge
                                       self.right_edge(governor_i)  # right_edge
                                       ))
        return self._dep_list

    def left_edge(self, index):
        left = index
        while True:
            children = self._graph_head_children.get(left, None)
            if children and (children[0][0] < left or left < 0):
                left = children[0][0]
            else:
                break
        if left < 0:
            raise ValueError('index out of range')
        return left

    def right_edge(self, index):
        right = index
        while True:
            children = self._graph_head_children.get(right, None)
            if children and right < children[-1][0]:
                right = children[-1][0]
            else:
                break
        if right > self._sent_length:
            raise ValueError('index out of range')
        return right

    def get_dep_tree(self, index=-1):
        if index < -1 or index >= self._sent_length:
            raise ValueError('index out of range')
        elif index == -1:
            if self._root_index == -1:
                return None
            else:
                index = self._root_index
        graph_vertex_status = ['O'] * self._sent_length
        return self._spanning_tree(graph_vertex_status, index)
        # Tree.fromstring(get_dep_tree()).draw()

    def _spanning_tree(self, visiting_array, node_index, node_name='ROOT'):
        visiting_array[node_index] = 'V'
        root = node_name  # dep_name
        subtrees = []
        leaf = self._leaf_func(self.tagged_list[node_index])
        if node_index not in self._graph_head_children:
            subtrees.append(leaf)
        else:
            subtrees.append(self._tree_func('^', [leaf]))
            this_pos = 0
            for child_i, child_name in self._graph_head_children[node_index]:
                if visiting_array[child_i] == 'V':
                    # has already visited
                    continue
                subtree = self._spanning_tree(visiting_array, child_i, child_name)
                if child_i < node_index:
                    subtrees.insert(this_pos, subtree)
                    this_pos += 1
                elif child_i > node_index:
                    subtrees.append(subtree)
        return self._tree_func(root, subtrees)


def _format_tree(root, subtree_list):
    return '(' + root + (' ' + ' '.join(subtree_list) if subtree_list else '') + ')'
    # from nltk.tree import Tree
    # return Tree(root, subtree_list)
