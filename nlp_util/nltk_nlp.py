# coding: utf-8

"""
Utility Tools for NLTK
======================

"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

from nltk import chunk
from nltk import pos_tag
from nltk import word_tokenize


def tag(text):
    """
    
    :param text: 
    :return: [(word, pos, chunck_ner, lemma), ...]
    """
    # nltk.download()  # models/punkt
    word_list = word_tokenize(text)
    # nltk.download()  # models/averaged_perceptron_tagger
    word_pos_list = pos_tag(word_list)
    # nltk.download()  # models/maxent_ne_chunker, corpora/words
    entities_tree = chunk.ne_chunk(word_pos_list)
    word_pos_chunck_list = chunk.util.tree2conlltags(entities_tree)
    return word_pos_chunck_list
