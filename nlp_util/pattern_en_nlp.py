# coding: utf-8

"""
Utility Tools for Pattern.en
============================
http://www.clips.ua.ac.be/pages/pattern-en

CLiPS (Computational Linguistics & Psycholinguistics) is a research center 
of University of Antwerp, Belgium.
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

# pattern.en
# noinspection PyUnresolvedReferences
import pattern.en


def kernel(text, parsing=True):
    tagged_str = pattern.en.parse(text,
                                  tokenize=True,  # Split punctuation marks from words?
                                  tags=True,  # Parse part-of-speech tags? (NN, JJ, ...)
                                  chunks=True,  # Parse chunks? (NP, VP, PNP, ...)
                                  relations=parsing,  # Parse chunk relations? (-SBJ, -OBJ, ...)
                                  lemmata=True,  # Parse lemmata? (ate => eat)
                                  encoding='utf-8',  # Input string encoding.
                                  tagset=None  # Penn Treebank II (default) or UNIVERSAL
                                  )
    return tagged_str


def tag(doc):
    """
    
    :param doc: 
    :return: yield [(word, pos, chunk, pnp-chunk, lemma), ...] of a sentence
    """
    tagged_str = kernel(doc, parsing=False)
    tagged_sents = tagged_str.split()
    # With chunks=True
    # each word is annotated with a chunk tag and a PNP tag (prepositional noun phrase, PP + NP).
    for tagged_list in tagged_sents:
        # [(word, pos, chunk, pnp-chunk, lemma), ...]
        yield tagged_list


def parse(doc):
    tagged_str = kernel(doc, parsing=True)
    parsed_sents = pattern.en.tree(tagged_str)

    for parsed_sent in parsed_sents:
        # [(word, pos, chunk, pnp-chunk, chunk-rol-relation, lemma), ...]
        tagged_list = [[w.string, w.type,
                        ('B-' if w.index == w.chunk.start else 'I-') + w.chunk.type
                        if w.chunk else 'O',
                        ('B-' if w.index == w.pnp.preposition.start else 'I-') + w.pnp.type
                        if w.pnp else 'O',
                        w.chunk.type + ('-' + w.chunk.role if w.chunk.role else '') +
                        '-' + str(w.chunk.relation)
                        if w.chunk and w.chunk.relation else 'O',
                        w.lemma]
                       for w in parsed_sent.words]

        # print(parsed_sent.relations)
        rdf_triples = []
        rel_list = ['SBJ', 'VP', 'OBJ']
        for i in range(1, max(map(len, map(parsed_sent.relations.get, rel_list))) + 1):
            triple = []
            for rel in rel_list:
                chunk = parsed_sent.relations[rel].get(i, None)
                if chunk:
                    triple.append(_format_tokens(chunk.words))
                else:
                    triple.append(None)
            if triple != [None, None, None]:
                rdf_triples.append(tuple(triple))
        yield (tagged_list, rdf_triples)


def _format_tokens(tokens):
    return ' '.join([token.string + '/' + token.type for token in tokens])
