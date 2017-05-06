# coding:utf-8

"""
Utility Tools for NLP
=====================
Demo of the interfaces of parts-of-speech tagging and dependency parsing.
Input: string
Tag output: tagged_list = [(word, pos, ...), (word, pos, ...), ...]
Parse output members: tagged_list, dep_list, dep_graph, root_index
Parse output functions: get_dep_tree, left_edge, right_edge
"""
# todo: syntaxnet
# TextBlob
# use NLTK and pattern.en library.

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

from pprint import pprint

# noinspection PyCompatibility
doc_en = (u'Vincent Willem van Gogh was a Dutch Post-Impressionist painter '
          u'who is among the most famous and influential figures in the history of Western art. '
          u'In just over a decade he created about 2,100 artworks, '
          u'including around 860 oil paintings, '
          u'most of them in the last two years of his life in France, where he died.\n '
          u'They include landscapes, still lives, portraits and self-portraits, '
          u'and are characterised by bold colours and dramatic, '
          u'impulsive and expressive brushwork that contributed to the foundations of modern art. '
          u'His suicide at 37 followed years of mental illness and poverty.')

# noinspection PyCompatibility
sent_en = (u'Vincent Willem van Gogh was a Dutch Post-Impressionist painter '
           u'who is among the most famous and influential figures in the history of Western art.')

# noinspection PyCompatibility
doc_zh = (u'莫奈（Claude Monet，1840年11月14日－1926年12月5日），'
          u'是法国最重要的画家之一，被誉为“印象派领导者”。'
          u'莫奈擅长光与影的实验与表现技法，他改变了阴影和轮廓线的绘画风格。\n '
          u'在莫奈的画作中看不到非常明确的阴影，也看不到突显或平涂式的轮廓线。')

# noinspection PyCompatibility
sent_zh = (u'莫奈（Claude Monet，1840年11月14日-1926年12月5日），'
           u'是法国最重要的画家之一，被誉为“印象派领导者”。')

"""
For English text
----------------

"""


def demo_nltk_nlp_tag_en():
    from nlp_util import nltk_nlp

    for tagged_list in nltk_nlp.tag_with_ssplit(doc_en):
        pprint(tagged_list)


def demo_stanford_nltk_tag_en():
    from nlp_util.stanford_nltk_nlp import StanfordNLP

    stanford_nlp = StanfordNLP('en')
    tagged_list = stanford_nlp.tag(sent_en)
    pprint(tagged_list)


def demo_stanford_nltk_parse_en():
    from nlp_util.stanford_nltk_nlp import StanfordNLP
    from nltk.tree import Tree

    stanford_nlp = StanfordNLP('en')
    for parsed_sent in stanford_nlp.parse_with_ssplit(doc_en):
        tagged_list = parsed_sent.tagged_list
        dep_list = parsed_sent.dep_list
        dep_tree = parsed_sent.get_dep_tree()
        pprint(tagged_list)
        pprint(dep_list)
        pprint(dep_tree)
        Tree.fromstring(dep_tree).draw()


def demo_stanford_corenlp_tag_en():
    from nlp_util.stanford_corenlp import StanfordNLP
    with StanfordNLP('en') as stanford_nlp:
        for tagged_list in stanford_nlp.tag_with_ssplit(doc_en):
            pprint(tagged_list)


def demo_stanford_corenlp_parse_en():
    from nlp_util.stanford_corenlp import StanfordNLP
    from nltk.tree import Tree
    with StanfordNLP('en') as stanford_nlp:
        for parsed_sent in stanford_nlp.parse_with_ssplit(doc_en):
            tagged_list = parsed_sent.tagged_list
            dep_list = parsed_sent.dep_list
            dep_tree = parsed_sent.get_dep_tree()
            pprint(tagged_list)
            pprint(dep_list)
            pprint(dep_tree)
            Tree.fromstring(dep_tree).draw()


def demo_stanford_corenlp_parse_en_without_ssplit():
    from nlp_util.stanford_corenlp import StanfordNLP
    from nltk.tree import Tree
    with StanfordNLP('en') as stanford_nlp:
        for parsed_sent in stanford_nlp.parse(doc_en):
            tagged_list = parsed_sent.tagged_list
            dep_list = parsed_sent.dep_list
            dep_tree = parsed_sent.get_dep_tree()
            pprint(tagged_list)
            pprint(dep_list)
            pprint(dep_tree)
            Tree.fromstring(dep_tree).draw()


def demo_spacy_nlp_tag_en():
    from nlp_util.spacy_nlp import SpaCyNLP
    nlp = SpaCyNLP()
    for tagged_list in nlp.tag(sent_en):
        pprint(tagged_list)


def demo_spacy_nlp_parse_en():
    from nlp_util.spacy_nlp import SpaCyNLP
    from nltk.tree import Tree
    nlp = SpaCyNLP()
    for parsed_sent in nlp.parse_with_ssplit(doc_en):
        tagged_list = parsed_sent.tagged_list
        dep_list = parsed_sent.dep_list
        dep_tree = parsed_sent.get_dep_tree()
        pprint(tagged_list)
        pprint(dep_list)
        pprint(dep_tree)
        Tree.fromstring(dep_tree).draw()
        pprint(parsed_sent.dep_graph)
        try:
            dep_tree = parsed_sent.get_dep_tree(6)
            Tree.fromstring(dep_tree).draw()
            dep_tree = parsed_sent.get_dep_tree(24)
            Tree.fromstring(dep_tree).draw()
            parsed_sent._leaf_func = lambda index: tagged_list[index][0]
            dep_tree = parsed_sent.get_dep_tree(parsed_sent.root_index)
            Tree.fromstring(dep_tree).draw()
        except ValueError as e:
            print(e.message)


def demo_antwerp_nlp_tag_en():
    from nlp_util import antwerp_nlp
    for tagged_list in antwerp_nlp.tag_with_ssplit(doc_en):
        pprint(tagged_list)


def demo_antwerp_nlp_parse_en():
    from nlp_util import antwerp_nlp
    for parsed_sent in antwerp_nlp.parse_with_ssplit(doc_en):
        tagged_list = parsed_sent.tagged_list
        rdf_triples = parsed_sent.get_rdf_triples()
        pprint(tagged_list)
        pprint(rdf_triples)


"""
For Chinese text
----------------

"""


def demo_jieba_nlp_tag_zh():
    from nlp_util import jieba_nlp

    tagged_list = jieba_nlp.tag(sent_zh)
    print_result(tagged_list)


def demo_jieba_nlp_tag_zh_with_parallel():
    from nlp_util import jieba_nlp
    from time import sleep
    with jieba_nlp.enable_parallel():
        for i in range(30):
            tagged_list = jieba_nlp.tag(sent_zh)
            print_result(tagged_list)
            sleep(1)


def demo_stanford_nltk_tag_zh():
    from nlp_util.stanford_nltk_nlp import StanfordNLP

    stanford_nlp = StanfordNLP('zh')
    tagged_list = stanford_nlp.tag(sent_zh)
    print_result(tagged_list)


def demo_stanford_nltk_parse_zh():
    from nlp_util.stanford_nltk_nlp import StanfordNLP
    from nltk.tree import Tree

    stanford_nlp = StanfordNLP('zh')
    try:
        for parsed_sent in stanford_nlp.parse(sent_zh):
            tagged_list = parsed_sent.tagged_list
            dep_list = parsed_sent.dep_list
            dep_tree = parsed_sent.get_dep_tree()
            print_result(tagged_list)
            pprint(dep_list)
            print(dep_tree.encode('utf-8'))
            Tree.fromstring(dep_tree).draw()
    except UnicodeDecodeError as e:
        print(e.message)


def demo_stanford_corenlp_tag_zh():
    from nlp_util.stanford_corenlp import StanfordNLP
    with StanfordNLP('zh') as stanford_nlp:
        for tagged_list in stanford_nlp.tag_with_ssplit(doc_zh):
            print_result(tagged_list)


def demo_stanford_corenlp_parse_zh():
    from nlp_util.stanford_corenlp import StanfordNLP
    from nltk.tree import Tree
    with StanfordNLP('zh') as stanford_nlp:
        for parsed_sent in stanford_nlp.parse_with_ssplit(doc_zh):
            tagged_list = parsed_sent.tagged_list
            dep_list = parsed_sent.dep_list
            dep_tree = parsed_sent.get_dep_tree()
            # pprint(parsed_sent.corenlp_sent)
            print_result(tagged_list)
            pprint(dep_list)
            print(dep_tree.encode('utf-8'))
            Tree.fromstring(dep_tree).draw()


def print_result(tagged_list):
    if tagged_list:
        if hasattr(tagged_list[0], '__iter__'):
            tagged_str = ' '.join(['_'.join(token) for token in tagged_list])
        else:
            tagged_str = ' '.join(tagged_list)
        print(tagged_str)


def show_demo():
    # import nlp_util.xxx

    # noinspection PyCompatibility
    # reload(nlp_util.xxx)
    # demo()
    demo_spacy_nlp_parse_en()


if __name__ == '__main__':
    show_demo()
