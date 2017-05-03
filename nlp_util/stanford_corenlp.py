# coding: utf-8

"""
Utility Tools for Stanford CoreNLP Server
=========================================
# standford_corenlp_server

"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

import os

from pycorenlp import StanfordCoreNLP


class StanfordCoreNLP(object):
    def __init__(self, lang='en'):  # lang = 'zh'
        self._stanford_nlp = None
        self._raw_output = None
        self._tagged_list = None
        self._dep_list = None
        self._arcs_dependent_governor = None
        self._graph_arcs_head_children = None

        def __enter__(self):
            self.set_up(lang)
            self._stanford_nlp = StanfordCoreNLP('http://localhost:9000')
            return self

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

    def _parse(self, text):
        corenlp_result = self._stanford_nlp.annotate(text, properties={
            'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, dcoref',
            'outputFormat': 'json'
        })

        # # result
        # print corenlp_result['sentences'][0].keys()
        # [u'tokens', u'index', u'parse',
        #  u'basicDependencies', u'enhancedDependencies', u'enhancedPlusPlusDependencies']

        # # parse
        # print(corenlp_result['sentences'][0]['parse'])
        # from nltk.tree import Tree
        #
        # sent_tree = Tree.fromstring(corenlp_result['sentences'][0]['parse'])
        # sent_tree.draw()

        self._raw_output = corenlp_result
        return self._raw_output

    def tag(self):
        # tokens
        # print self._raw_output['sentences'][0]['tokens'][0].keys()
        # [u'index', u'word', u'lemma', u'originalText', u'pos', u'before', u'after',
        #  u'characterOffsetEnd', u'characterOffsetBegin', u'ner', u'speaker']
        tagged_list = [(t['word'], t['pos'], t['ner'], t['speaker'], t['lemma']) for t in
                       self._raw_output['sentences'][0]['tokens']]
        return tagged_list


    def dep(self):
        # dependencies
        # basicDependencies, enhancedDependencies, enhancedPlusPlusDependencies
        dependencies = self._raw_output['sentences'][0]['enhancedPlusPlusDependencies']
        self._arcs_dependent_governor = [list() for _ in range(len(self._tagged_list))]
        self._graph_arcs_head_children = dict()
        for d in dependencies:
            dependent_i = d['dependent'] - 1
            dep_name = d['dep']
            governor_i = d['governor'] - 1
            arc_length = abs(dependent_i - governor_i) if governor_i > 0 else 0
            self._arcs_dependent_governor[dependent_i].append((arc_length, dep_name, governor_i))
            self._graph_arcs_head_children.setdefault(governor_i, list()).append((dependent_i, dep_name))

        for head in self._graph_arcs_head_children:
            self._graph_arcs_head_children[head].sort()

        def left_edge(index):
            left = index
            while True:
                children = graph_arcs_head_children.get(left, None)
                if children and (children[0][0] < left or left < 0):
                    left = children[0][0]
                else:
                    break
            return left

        def right_edge(index):
            right = index
            while True:
                children = graph_arcs_head_children.get(right, None)
                if children and right < children[-1][0]:
                    right = children[-1][0]
                else:
                    break
            return right

        dep_list = []
        for dependent_i, arc_list in enumerate(self._arcs_dependent_governor):
            arc_shortest = sorted(arc_list)[0] if len(arc_list) > 1 else arc_list[0]
            dep_name = arc_shortest[1]
            governor_i = arc_shortest[2]
            dep_list.append((dep_name,  # dep_name name
                             governor_i if governor_i > 0 else dependent_i,  # head
                             left_edge(governor_i),  # left_edge
                             right_edge(governor_i) + 1  # right_edge + 1
                             ))

        return dep_list

    def _spanning_tree(self, node_visiting_list, node_index, node_name='ROOT',
                      construct_tree_func=format_tree,
                      construct_leaf_func=format_leaf):
        node_visiting_list[node_index] = 'V'
        root = node_name  # dep_name
        subtrees = []
        leaf = construct_leaf_func(self._tagged_list[node_index])
        if node_index not in self._graph_arcs_head_children:
            subtrees.append(leaf)
        else:
            subtrees.append(construct_tree_func('^', [leaf]))
            left_tree_pos = 0
            for child_i, child_name in self._graph_arcs_head_children[node_index]:
                if node_visiting_list[child_i] == 'V':
                    continue
                subtree = self._spanning_tree(node_visiting_list, child_i, child_name)
                if child_i < node_index:
                    subtrees.insert(left_tree_pos, subtree)
                    left_tree_pos += 1
                elif child_i > node_index:
                    subtrees.append(subtree)
        return construct_tree_func(root, subtrees)


    def get_dep_tree_str(self, index):
        graph_vertex_status = ['O'] * len(self._dep_list)
        return self._spanning_tree(graph_vertex_status, index)



def format_tree(root, subtree_list):
    return '(' + root + (' ' + ' '.join(subtree_list) if subtree_list else '') + ')'


def format_leaf(token):
    return '/'.join([token[0].replace('(', u'（').replace('(', u'）'),
                     token[1].replace('(', u'（').replace('(', u'）')])



sent_tree = get_dep_tree_str(-1)
from nltk.tree import Tree
Tree.fromstring(sent_tree).draw()
