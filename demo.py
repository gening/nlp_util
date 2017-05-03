# coding:utf-8

"""
Utility Tools for NLP
=====================
Unified Interface of parts-of-speech tagging and dependency parsing.
Input: string
Output: [(word, pos, ...), (word, pos, ...), ...]
"""
# todo: dependencies parse of stanford nltk
# todo: syntaxnet

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

text = (u'Vincent Willem van Gogh was a Dutch Post-Impressionist painter '
        u'who is among the most famous and influential figures in the history of Western art. '
        u'In just over a decade he created about 2,100 artworks, '
        u'including around 860 oil paintings, '
        u'most of them in the last two years of his life in France, where he died. '
        u'They include landscapes, still lifes, portraits and self-portraits, '
        u'and are characterised by bold colours and dramatic, '
        u'impulsive and expressive brushwork that contributed to the foundations of modern art. '
        u'His suicide at 37 followed years of mental illness and poverty.')

text = (u'Vincent Willem van Gogh was a Dutch Post-Impressionist painter '
        u'who is among the most famous and influential figures in the history of Western art.')



# syntaxnet
# todo

# TextBlob
# use NLTK and pattern.en library.
