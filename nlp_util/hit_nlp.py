# coding: utf-8

"""
Utility Tools for HIT-SCIR LTP
==============================
https://github.com/HIT-SCIR/pyltp
http://www.ltp-cloud.com/

Language Technology Platform (LTP）of Harbin Institute of Technology, China
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"

from pyltp import SentenceSplitter

from . import conf

cfg = conf('hit_nlp.conf').get


def get_segmentor():
    from pyltp import Segmentor
    cws_model = cfg('model', 'cws_model').encode('utf-8')
    # noinspection PyArgumentList
    segmentor = Segmentor()
    segmentor.load(cws_model)
    return segmentor


def get_pos_tagger():
    from pyltp import Postagger
    pos_model = cfg('model', 'pos_model').encode('utf-8')
    # noinspection PyArgumentList
    postagger = Postagger()
    postagger.load(pos_model)
    return postagger


def get_ner_tagger():
    from pyltp import NamedEntityRecognizer
    ner_model = cfg('model', 'ner_model').encode('utf-8')
    # noinspection PyArgumentList
    recognizer = NamedEntityRecognizer()
    recognizer.load(ner_model)
    return recognizer


def get_dep_parser():
    from pyltp import Parser
    parser_model = cfg('model', 'parser_model').encode('utf-8')
    # noinspection PyArgumentList
    parser = Parser()
    parser.load(parser_model)
    return parser


def get_role_labeller():
    srl_model_path = cfg('model', 'srl_model_path').encode('utf-8')
    from pyltp import SementicRoleLabeller
    # noinspection PyArgumentList
    labeller = SementicRoleLabeller()
    labeller.load(srl_model_path)
    return labeller


class HITNLP(object):
    def __init__(self, parsing=True):
        self.parsing = parsing
        self.segmentor = None
        self.postagger = None
        self.recognizer = None
        self.parser = None
        self.labeller = None

    def __enter__(self):
        try:
            self.segmentor = get_segmentor()
            self.postagger = get_pos_tagger()
            self.recognizer = get_ner_tagger()
            if self.parsing:
                self.parser = get_dep_parser()
                # self.labeller = get_role_labeller()
        except Exception:
            raise Exception('fail to load ltp data of models')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.segmentor:
            self.segmentor.release()
        if self.postagger:
            self.postagger.release()
        if self.recognizer:
            self.recognizer.release()
        if self.parser:
            self.parser.release()
        if self.labeller:
            self.labeller.release()

    def tag_with_ssplit(self, doc):
        # noinspection PyArgumentList
        sents = SentenceSplitter.split(doc.encode('utf-8'))
        for sent in sents:
            sent = sent.strip()
            if len(sent) == 0:
                continue
            words = self.segmentor.segment(sent)
            pos_tags = self.postagger.postag(words)
            ner_tags = self.recognizer.recognize(words, pos_tags)

            word_pos_ner_list = []
            for i in range(len(words)):
                word = words[i].decode('utf-8')
                pos = pos_tags[i].decode('utf-8')
                ner = ner_tags[i].decode('utf-8')
                word_pos_ner_list.append((word, pos, ner))
            yield word_pos_ner_list

    def parse_with_ssplit(self, doc):
        if not self.parsing:
            self.parsing = True
            self.parser = get_dep_parser()
            # self.labeller = get_role_labeller()

        # noinspection PyArgumentList
        sents = SentenceSplitter.split(doc.encode('utf-8'))
        for sent in sents:
            sent = sent.strip()
            if len(sent) == 0:
                continue
            words = self.segmentor.segment(sent)
            pos_tags = self.postagger.postag(words)
            ner_tags = self.recognizer.recognize(words, pos_tags)

            arcs = self.parser.parse(words, pos_tags)
            # roles = self.labeller.label(words, pos_tags, ner_tags, arcs)

            word_pos_ner_list = []
            for i in range(len(words)):
                word = words[i].decode('utf-8')
                pos = pos_tags[i].decode('utf-8')
                ner = ner_tags[i].decode('utf-8')
                word_pos_ner_list.append((word, pos, ner))
            yield ParsedSent(word_pos_ner_list, arcs)


from interface import DependencyGraphI


class ParsedSent(DependencyGraphI):
    def __init__(self, word_pos_ner_list, ltp_arcs):
        super(self.__class__, self).__init__(make_leaf=self._leaf_func)
        # raw result
        self.ltp_arcs = ltp_arcs
        # tokens
        self.tagged_list = word_pos_ner_list
        # dependency graph
        node_num = len(self.ltp_arcs)
        self.dep_graph, self.root_index = self._build_dep_graph(node_num)

    def _build_dep_graph(self, node_num):
        # dependency graph
        root_index = None
        self._dep_graph = [dict() for _ in range(node_num)]
        for index, arc in enumerate(self.ltp_arcs):
            dep_index = index
            dep_rel = arc.relation
            head_index = arc.head - 1 if arc.head != 0 else dep_index
            # option `enhancedPlusPlusDependencies` may cause one mapped to two heads.
            root_index = self._add_dep_arc(dep_index, dep_rel, head_index)
        return self._dep_graph, root_index

    def _leaf_func(self, index):
        token = self.tagged_list[index]
        # noinspection PyCompatibility
        return '/'.join([token[0], token[1]]).replace('(', u'（').replace('(', u'）')
