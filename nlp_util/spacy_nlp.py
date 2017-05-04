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


class SpaCyNLP(object):
    def __init__(self, lang='en'):
        self._spacy_nlp = spacy.load(conf[lang])

    def kernel(self, doc, parsing=True):
        if parsing:
            spacy_doc = self._spacy_nlp(doc)
        else:
            spacy_doc = self._spacy_nlp(doc, parse=False)
        return spacy_doc

    def tag(self, doc):
        spacy_doc = self.kernel(doc, parsing=False)
        for spacy_sent in spacy_doc.sents:
            tagged_list = [(t.text, t.tag_, t.ent_iob_, t.ent_type_, t.lemma_) for t in spacy_sent]
            yield tagged_list

    def parse(self, doc):
        spacy_doc = self.kernel(doc)
        for spacy_sent in spacy_doc.sents:
            yield SentDependency(spacy_sent)


class SentDependency(object):
    def __init__(self, spacy_sent):
        self.spacy_sent = spacy_sent
        self._offset = spacy_sent.start
        self.tagged_list = [(t.text, t.tag_, t.ent_iob_, t.ent_type_, t.lemma_) for t in spacy_sent]
        self.dep_list = [(t.dep_,  # dep name
                          t.head.i - self._offset,  # head
                          t.left_edge.i - self._offset,  # left_edge
                          t.right_edge.i - self._offset  # right_edge
                          ) for t in spacy_sent]
        self._tree_func = _format_tree
        self._leaf_func = lambda token: '/'.join([token.orth_, token.tag_])

    def left_edge(self, index):
        space_token = self.spacy_sent[index]
        return space_token.left_edge.i - self._offset

    def right_edge(self, index):
        space_token = self.spacy_sent[index]
        return space_token.right_edge.i - self._offset

    def get_dep_tree(self, index=-1):
        if index == -1:
            # If there's a forest, the earliest is preferred
            spacy_token = self.spacy_sent.root
        else:
            spacy_token = self.spacy_sent[index]  # fixme: index out of range
        # if index < -1 or index > self.spacy_sent.end - self.spacy_sent.start:
        #     raise ValueError('index out of range')
        graph_vertex_status = ['O'] * (self.spacy_sent.end - self.spacy_sent.start + 1)
        return self._spanning_tree(graph_vertex_status, spacy_token)
        # Tree.fromstring(get_dep_tree()).draw()

    def _spanning_tree(self, visiting_array, node):
        if self.spacy_sent.start <= node.i <= self.spacy_sent.start.end:
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
        leaf = self._leaf_func(node)
        if len(subtrees) > 0:
            subtrees.insert(this_pos, self._tree_func('^', [leaf]))
        else:
            subtrees.insert(this_pos, leaf)
        return self._tree_func(root, subtrees)


def _format_tree(root, subtree_list):
    return '(' + root + (' ' + ' '.join(subtree_list) if subtree_list else '') + ')'
    # from nltk.tree import Tree
    # return Tree(root, subtree_list)
