# coding:utf-8

"""
Utility Tools for NLP
=====================
Unified Interface of parts-of-speech tagging and dependency parsing.
Input: string
Output: [(word, pos, ...), (word, pos, ...), ...]
"""
# todo: test
# todo: dependencies parse of stanford nltk
# todo: syntaxnet
# TextBlob
# use NLTK and pattern.en library.

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

# noinspection PyCompatibility
doc_en = (u'Vincent Willem van Gogh was a Dutch Post-Impressionist painter '
          u'who is among the most famous and influential figures in the history of Western art.\n '
          u'In just over a decade he created about 2,100 artworks, '
          u'including around 860 oil paintings, '
          u'most of them in the last two years of his life in France, where he died. '
          u'They include landscapes, still lives, portraits and self-portraits, '
          u'and are characterised by bold colours and dramatic, '
          u'impulsive and expressive brushwork that contributed to the foundations of modern art. '
          u'His suicide at 37 followed years of mental illness and poverty.')

# noinspection PyCompatibility
sent_en = (u'Vincent Willem van Gogh was a Dutch Post-Impressionist painter '
           u'who is among the most famous and influential figures in the history of Western art.')

# noinspection PyCompatibility
doc_zh = (u'莫奈（Claude Monet，1840年11月14日－1926年12月5日），'
          u'是法国最重要的画家之一，被誉为“印象派领导者”。\n'
          u'莫奈擅长光与影的实验与表现技法，他改变了阴影和轮廓线的绘画风格。'
          u'在莫奈的画作中看不到非常明确的阴影，也看不到突显或平涂式的轮廓线。')

# noinspection PyCompatibility
sent_zh = (u'莫奈（Claude Monet，1840年11月14日－1926年12月5日），'
           u'是法国最重要的画家之一，被誉为“印象派领导者”。')
