# coding: utf-8

"""
Utility Tools for spaCy
=======================

"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

import spacy

model = {'en': 'en_core_web_md'}


class SpaCyNLP(object):
    def __init__(self, lang='en', parse=True):
        if parse:
            self._spacy_nlp = spacy.load(model[lang])
        else:
            self._spacy_nlp = spacy.load(model[lang], parser=False)

    def core(self, text, parse=True):
        if parse:
            doc = self._spacy_nlp(text)
        else:
            doc = self._spacy_nlp(text, parse=False)

    def tag(self, text):
        tagged_list = [(t.text, t.tag_, t.ent_iob_, t.ent_type_, t.lemma_) for t in doc]
        return tagged_list

    def dep(self, text):
        offset = doc[0].i
        dep_list = [(t.dep_, t.head.i - offset, t.left_edge.i - offset, t.right_edge.i + 1 - offset)
                    for t in doc]
        return dep_list

    def get_dep_tree_str(self, index):
        graph_vertex_status = ['O'] * len(self._dep_list)
        return self._spanning_tree(graph_vertex_status, index)

    # fixme loop
    def _spanning_tree(self, node,
                       construct_tree_func=format_tree, construct_leaf_func=format_leaf):
        root = node.dep_
        subtrees = []
        subtrees.extend([self._spanning_tree(child) for child in node.lefts])
        if node.n_lefts + node.n_rights > 0:
            subtrees.append(construct_tree_func('^', [format_leaf(node)]))
        else:
            subtrees.append(construct_leaf_func(node))
        subtrees.extend([self._spanning_tree(child) for child in node.rights])
        return construct_tree_func(root, subtrees)


def format_leaf(token):
    return '/'.join([token.orth_, token.tag_])


def format_tree(root, subtree_list):
    return '(' + root + (' ' + ' '.join(subtree_list) if subtree_list else '') + ')'


sent_trees = sum([[get_dep_tree_str(sent.root) for sent in doc.sents]], [])

from nltk.tree import Tree

for sent_tree in sent_trees:
    Tree.fromstring(sent_tree).draw()

    # spacy with deep learning
    # https://spacy.io/docs/usage/tutorials
