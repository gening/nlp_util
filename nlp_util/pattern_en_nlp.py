# coding: utf-8

"""
Utility Tools for Pattern.en
============================

"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

# pattern.en
# noinspection PyUnresolvedReferences
from pattern.en import parse


def tag(text):
    """
    
    :param text: 
    :return: [(word, pos, np-chunk, pnp-chunk, rel, lemma), ...]
    """
    tagged_list = parse(text,
                        tokenize=True,  # Split punctuation marks from words?
                        tags=True,  # Parse part-of-speech tags? (NN, JJ, ...)
                        chunks=True,  # Parse chunks? (NP, VP, PNP, ...)
                        relations=True,  # Parse chunk relations? (-SBJ, -OBJ, ...)
                        lemmata=True,  # Parse lemmata? (ate => eat)
                        encoding='utf-8',  # Input string encoding.
                        tagset=None  # Penn Treebank II (default) or UNIVERSAL
                        ).split()[0]
    # With chunks=True
    # each word is annotated with a chunk tag and a PNP tag (prepositional noun phrase, PP + NP).
    return tagged_list


# noinspection PyUnresolvedReferences
from pattern.en import parsetree


def format_tokens(tokens):
    return ' '.join([token.string + '/' + token.type for token in tokens])


def get_ref_triples(text):
    sent_trees = parsetree(text,
                           tokenize=True,  # Split punctuation marks from words?
                           tags=True,  # Parse part-of-speech tags? (NN, JJ, ...)
                           chunks=True,  # Parse chunks? (NP, VP, PNP, ...)
                           relations=True,  # Parse chunk relations? (-SBJ, -OBJ, ...)
                           lemmata=True,  # Parse lemmata? (ate => eat)
                           encoding='utf-8',  # Input string encoding.
                           tagset=None  # Penn Treebank II (default) or UNIVERSAL
                           )

    rdf_triples = []
    for sent_tree in sent_trees:
        print(sent_tree.relations)
        rel_list = ['SBJ', 'VP', 'OBJ']
        for i in range(1, max(map(len, map(sent_tree.relations.get, rel_list))) + 1):
            triple = []
            for rel in rel_list:
                chunk = sent_tree.relations[rel].get(i, None)
                if chunk:
                    triple.append(format_tokens(chunk.words))
                else:
                    triple.append(None)
            if triple != [None, None, None]:
                rdf_triples.append(tuple(triple))
    return rdf_triples
