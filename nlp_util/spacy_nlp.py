# coding: utf-8

"""
Utility Tools for spaCy
=======================
https://spacy.io/

spaCy is a Industrial-Strength Natural Language Processing Library of Python, 
developed by Explosion AI which is a digital studio in Berlin, Germany 
specialising in Artificial Intelligence.

To use spaCy with Machine Learning, please see: https://spacy.io/docs/usage/tutorials
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

import spacy

conf = {'en': 'en_core_web_md'}


def _tagged_tuple(token):
    token_tuple = [token.text,
                   token.tag_,
                   token.ent_iob_,
                   token.ent_type_,
                   token.lemma_]
    return token_tuple


class SpaCyNLP(object):
    def __init__(self, lang='en'):
        self._spacy_nlp = spacy.load(conf[lang])

    def annotate(self, doc, parsing=True):
        if parsing:
            spacy_doc = self._spacy_nlp(doc)
        else:
            spacy_doc = self._spacy_nlp(doc, parse=False)
        return spacy_doc

    def tag(self, text):
        # sentence boundary detection requires the dependency parse
        spacy_doc = self.annotate(text, parsing=False)
        tagged_list = [_tagged_tuple(t) for t in spacy_doc]
        return tagged_list

    def parse_with_ssplit(self, doc):
        spacy_doc = self.annotate(doc)
        for spacy_sent in spacy_doc.sents:
            yield ParsedSent(spacy_sent)


class ParsedSent(object):
    # Usage of Index:
    # given that spacy_doc and spacy_sent are the instance of SpaCy Doc and Sent respectively,
    # when i >= 0, spacy_sent[i] will return the token of spacy_doc[spacy_sent.start + i].
    # when i < 0, spacy_sent[i] will return the token of spacy_doc[spacy_sent.end + i].
    # when j >= len(spacy_doc) or j < -len(spacy_doc), an IndexError should be raised.
    # token.i = spacy_doc[i].i, whereas spacy_sent[i].i = spacy_doc[i + spacy_sent.start].i
    def __init__(self, spacy_sent):
        self.spacy_sent = spacy_sent
        self._offset = spacy_sent.start
        self.tagged_list = [_tagged_tuple(t) for t in spacy_sent]
        self.dep_list = [(t.dep_,  # dep name
                          t.head.i - self._offset,  # head
                          t.left_edge.i - self._offset,  # start = left_edge
                          t.right_edge.i - self._offset  # end = right_edge + 1
                          ) for t in spacy_sent]
        self.dep_graph, self.root_index = self._build_dep_graph(spacy_sent.end - spacy_sent.start)
        self._tree_func = _format_tree
        # self._leaf_func defined as function, which is also an attr of class.

    def _build_dep_graph(self, node_num):
        # raise NotImplementedError('ParsedSent.')
        dep_graph = [dict() for _ in range(node_num)]
        for spacy_token in self.spacy_sent:
            index = spacy_token.i - self._offset
            dep_graph[index]['rel'] = spacy_token.dep_
            dep_graph[index]['head'] = spacy_token.head.i
            for token_dep in spacy_token.children:
                if self.spacy_sent.start <= token_dep.i < self.spacy_sent.end:
                    dep_graph[index].setdefault('deps', dict()
                                                ).setdefault(token_dep.dep_, list()
                                                             ).append(token_dep.i - self._offset)

        root_index = self.spacy_sent.root.i
        return dep_graph, root_index

    def left_edge(self, index):
        if index < 0 or index >= self.spacy_sent.end - self.spacy_sent.start:
            raise ValueError('index out of range')
        space_token = self.spacy_sent[index]
        return space_token.left_edge.i - self._offset

    def right_edge(self, index):
        if index < 0 or index >= self.spacy_sent.end - self.spacy_sent.start:
            raise ValueError('index out of range')
        space_token = self.spacy_sent[index]
        return space_token.right_edge.i - self._offset

    def get_dep_tree(self, index=None):
        if index is None:
            # If there's a forest, the earliest is preferred
            spacy_token = self.spacy_sent.root
        elif index < 0 or index >= self.spacy_sent.end - self.spacy_sent.start:
            raise ValueError('index out of range')
        else:
            spacy_token = self.spacy_sent[index]
        graph_vertex_status = ['O'] * (self.spacy_sent.end - self.spacy_sent.start)
        return self._spanning_tree(graph_vertex_status, spacy_token)
        # from nltk.tree import Tree
        # Tree.fromstring(get_dep_tree()).draw()

    def _spanning_tree(self, visiting_array, node):
        if self.spacy_sent.start <= node.i < self.spacy_sent.end:
            index = node.i - self._offset
            if visiting_array[index] != 'V':
                visiting_array[index] = 'V'
            else:
                # has already visited
                return None
        else:
            # index of ouf sent range
            return None
        root = node.dep_
        subtrees = []
        this_pos = 0
        # left
        for child in node.lefts:
            subtree = self._spanning_tree(visiting_array, child)
            if subtree:
                subtrees.append(subtree)
                this_pos += 1
        # right
        for child in node.rights:
            subtree = self._spanning_tree(visiting_array, child)
            if subtree:
                subtrees.append(subtree)
        # this
        leaf = self._leaf_func(node.i - self._offset)
        if len(subtrees) > 0:
            subtrees.insert(this_pos, self._tree_func('^', [leaf]))
        else:
            subtrees.insert(this_pos, leaf)
        return self._tree_func(root, subtrees)

    def _leaf_func(self, index):
        token = self.spacy_sent[index]
        return '/'.join([token.orth_, token.tag_])


def _format_tree(root_label, subtree_list):
    return '(' + root_label + (' ' + ' '.join(subtree_list) if subtree_list else '') + ')'
    # from nltk.tree import Tree
    # return Tree(root_label, subtree_list)


"""
dep_graph = 
[{'head': 3, 'rel': u'compound'},
 {'head': 3, 'rel': u'compound'},
 {'head': 3, 'rel': u'compound'},
 {'deps': {u'compound': [0, 1, 2]}, 'head': 4, 'rel': u'nsubj'},
 {'deps': {u'attr': [10], u'nsubj': [3], u'punct': [26]},
  'head': 4,
  'rel': u'ROOT'},
 {'head': 10, 'rel': u'det'},
 {'head': 10, 'rel': u'amod'},
 {'head': 9, 'rel': u'compound'},
 {'head': 9, 'rel': u'punct'},
 {'deps': {u'compound': [7], u'punct': [8]}, 'head': 10, 'rel': u'compound'},
 {'deps': {u'amod': [6], u'compound': [9], u'det': [5], u'relcl': [12]},
  'head': 4,
  'rel': u'attr'},
 {'head': 12, 'rel': u'nsubj'},
 {'deps': {u'nsubj': [11], u'prep': [13]}, 'head': 10, 'rel': u'relcl'},
 {'deps': {u'pobj': [19]}, 'head': 12, 'rel': u'prep'},
 {'head': 19, 'rel': u'det'},
 {'head': 16, 'rel': u'advmod'},
 {'deps': {u'advmod': [15], u'cc': [17], u'conj': [18]},
  'head': 19,
  'rel': u'amod'},
 {'head': 16, 'rel': u'cc'},
 {'head': 16, 'rel': u'conj'},
 {'deps': {u'amod': [16], u'det': [14], u'prep': [20]},
  'head': 13,
  'rel': u'pobj'},
 {'deps': {u'pobj': [22]}, 'head': 19, 'rel': u'prep'},
 {'head': 22, 'rel': u'det'},
 {'deps': {u'det': [21], u'prep': [23]}, 'head': 20, 'rel': u'pobj'},
 {'deps': {u'pobj': [25]}, 'head': 22, 'rel': u'prep'},
 {'head': 25, 'rel': u'amod'},
 {'deps': {u'amod': [24]}, 'head': 23, 'rel': u'pobj'},
 {'head': 4, 'rel': u'punct'}]
"""
