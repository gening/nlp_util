# coding:utf-8

"""
Utility Tools for Jieba
=======================
# jieba 结巴分词

"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

from jieba import enable_parallel

enable_parallel(4)

from jieba import posseg


def tag(cls, text):
    """
    
    :param text: 
    :return: [(word, pos), ...]
    """
    word_pos_list = [(word, pos) for word, pos in posseg.cut(text)]
    return word_pos_list
