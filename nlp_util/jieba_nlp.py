# coding:utf-8

"""
Utility Tools for Jieba
=======================
https://github.com/fxsjy/jieba

"Jieba" (Chinese for "to stutter") Chinese text segmentation
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

from jieba import enable_parallel

enable_parallel(4)  # fixme: disable_parallel()

from jieba import posseg


def tag(text):
    """
    
    :param text: 
    :return: [(word, pos), ...]
    """
    word_pos_list = [(word, pos) for word, pos in posseg.cut(text)]
    return word_pos_list
