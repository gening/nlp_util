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
# todo: doc
# todo: provide conll_10 interface
# todo: import python package -- auto check
# todo: check model data -- auto config or download gzip
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


def print_parsed_result_en(parsed_sent):
    from nltk.tree import Tree
    tagged_list = parsed_sent.tagged_list
    dep_list = parsed_sent.dep_list
    dep_tree = parsed_sent.get_dep_tree()
    pprint(tagged_list)
    pprint(dep_list)
    pprint(dep_tree)
    Tree.fromstring(dep_tree).draw()


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
    stanford_nlp = StanfordNLP('en')
    for parsed_sent in stanford_nlp.parse_with_ssplit(doc_en):
        print_parsed_result_en(parsed_sent)


def demo_stanford_corenlp_tag_en():
    from nlp_util.stanford_corenlp import StanfordNLP
    with StanfordNLP('en') as stanford_nlp:
        for tagged_list in stanford_nlp.tag_with_ssplit(doc_en):
            pprint(tagged_list)


def demo_stanford_corenlp_parse_en():
    from nlp_util.stanford_corenlp import StanfordNLP
    with StanfordNLP('en') as stanford_nlp:
        for parsed_sent in stanford_nlp.parse_with_ssplit(doc_en):
            print_parsed_result_en(parsed_sent)


def demo_stanford_corenlp_parse_en_without_ssplit():
    from nlp_util.stanford_corenlp import StanfordNLP
    with StanfordNLP('en') as stanford_nlp:
        for parsed_sent in stanford_nlp.parse(doc_en):
            print_parsed_result_en(parsed_sent)


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
        pprint(parsed_sent.dep_graph)
        print_parsed_result_en(parsed_sent)
        try:
            tagged_list = parsed_sent.tagged_list
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


def demo_tf_dragnn_nlp_parse_en():
    from nlp_util.tensorflow_dragnn_nlp import TfDragnnNLP
    tf_dragnn_nlp = TfDragnnNLP('en')
    # noinspection PyShadowingNames
    for sent_en in doc_en.replace('\n', '').split('. '):
        parsed_sent = tf_dragnn_nlp.parse(sent_en)
        print_parsed_result_en(parsed_sent)

    dragnn_sent, dragnn_trace_str = tf_dragnn_nlp.annotate("John is eating pizza with a fork")
    # Also try: John is eating pizza with a fork
    from nlp_util.tensorflow_dragnn_nlp import ParsedSent
    # noinspection PyProtectedMember
    from nlp_util.tensorflow_dragnn_nlp import _parse_tree_explorer
    # noinspection PyProtectedMember
    from nlp_util.tensorflow_dragnn_nlp import _trace_explorer
    # noinspection PyProtectedMember
    from nlp_util.tensorflow_dragnn_nlp import _browse_html
    lookup_dict, node_num = ParsedSent.comprehend_dragnn_sent(dragnn_sent)
    pprint(dragnn_sent)
    pprint(lookup_dict)
    pprint(node_num)
    neural_graph_html = _trace_explorer(dragnn_trace_str)
    _browse_html(neural_graph_html, 'temp_dragnn_graph.html')
    dependency_tree_html = _parse_tree_explorer(dragnn_sent)
    _browse_html(dependency_tree_html, 'temp_dragnn_tree.html')


"""
For Chinese text
----------------

"""


def print_tagged_result_zh(tagged_list):
    if tagged_list:
        if hasattr(tagged_list[0], '__iter__'):
            tagged_str = ' '.join(['_'.join(map(unicode, token)) for token in tagged_list])
        else:
            tagged_str = ' '.join(tagged_list)
        print(tagged_str)


def print_parsed_result_zh(parsed_sent):
    from nltk.tree import Tree
    tagged_list = parsed_sent.tagged_list
    dep_list = parsed_sent.dep_list
    dep_tree = parsed_sent.get_dep_tree()
    print_tagged_result_zh(tagged_list)
    pprint(dep_list)
    print(dep_tree.encode('utf-8'))
    Tree.fromstring(dep_tree).draw()


def demo_jieba_nlp_tag_zh():
    from nlp_util import jieba_nlp
    tagged_list = jieba_nlp.tag(sent_zh)
    print_tagged_result_zh(tagged_list)


def demo_jieba_nlp_tag_zh_with_parallel():
    from nlp_util import jieba_nlp
    from time import sleep
    with jieba_nlp.enable_parallel():
        for i in range(30):
            tagged_list = jieba_nlp.tag(sent_zh)
            print_tagged_result_zh(tagged_list)
            sleep(1)


def demo_hit_nlp_tag_zh():
    import sys
    import time
    from nlp_util.hit_nlp import HITNLP
    with HITNLP() as hit_nlp:
        texts = [doc_zh, sent_zh]
        iter_texts = (texts[i % 2] for i in range(400))
        print(time.ctime())
        for i, text in enumerate(iter_texts):
            for tagged_list in hit_nlp.tag_with_ssplit(text):
                sys.stdout.write('%3d\t' % i)
                print_tagged_result_zh(tagged_list)
                pass
        print(time.ctime())


def demo_hit_nlp_parse_zh():
    from nlp_util.hit_nlp import HITNLP
    with HITNLP() as hit_nlp:
        for parsed_sent in hit_nlp.parse_with_ssplit(doc_zh):
            print_parsed_result_zh(parsed_sent)


def demo_stanford_nltk_tag_zh():
    from nlp_util.stanford_nltk_nlp import StanfordNLP
    stanford_nlp = StanfordNLP('zh')
    tagged_list = stanford_nlp.tag(sent_zh)
    print_tagged_result_zh(tagged_list)


def demo_stanford_nltk_parse_zh():
    from nlp_util.stanford_nltk_nlp import StanfordNLP
    stanford_nlp = StanfordNLP('zh')
    try:
        parsed_sent = stanford_nlp.parse(sent_zh)
        if parsed_sent:
            print_parsed_result_zh(parsed_sent)
    except UnicodeDecodeError as e:
        print(e.message)


def demo_stanford_corenlp_tag_zh():
    from nlp_util.stanford_corenlp import StanfordNLP
    with StanfordNLP('zh') as stanford_nlp:
        for tagged_list in stanford_nlp.tag_with_ssplit(doc_zh):
            print_tagged_result_zh(tagged_list)


def demo_stanford_corenlp_parse_zh():
    from nlp_util.stanford_corenlp import StanfordNLP
    with StanfordNLP('zh') as stanford_nlp:
        for parsed_sent in stanford_nlp.parse_with_ssplit(doc_zh):
            print_parsed_result_zh(parsed_sent)


def demo_tf_dragnn_nlp_parse_zh():
    from nlp_util.tensorflow_dragnn_nlp import TfDragnnNLP
    tf_dragnn_nlp = TfDragnnNLP('zh')
    # noinspection PyCompatibility, PyShadowingNames
    for sent_chi in doc_zh.replace('\n', '').split(u'。'):
        sent_chi = sent_chi.strip()
        if sent_chi != '':
            # noinspection PyCompatibility
            parsed_sent = tf_dragnn_nlp.parse(sent_chi + u'。')
            print_parsed_result_zh(parsed_sent)


def show_demo():
    # import nlp_util.xxx

    # noinspection PyCompatibility
    # reload(nlp_util.xxx)
    # demo()
    demo = 'demo_nltk_nlp_tag_en'
    import timeit
    print(timeit.timeit(demo + '()', setup='from __main__ import ' + demo, number=1))


if __name__ == '__main__':
    show_demo()
