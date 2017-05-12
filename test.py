# coding:utf-8

"""
Utility Tools for NLP
=====================
Test parse interfaces.
"""
from pprint import pprint

# noinspection PyCompatibility
corenlp_sent = {
    u'basicDependencies': [
        {u'dep': u'ROOT', u'dependent': 9, u'governorGloss': u'ROOT', u'governor': 0,
         u'dependentGloss': u'painter'},
        {u'dep': u'compound', u'dependent': 1, u'governorGloss': u'Gogh', u'governor': 4,
         u'dependentGloss': u'Vincent'},
        {u'dep': u'compound', u'dependent': 2, u'governorGloss': u'Gogh', u'governor': 4,
         u'dependentGloss': u'Willem'},
        {u'dep': u'compound', u'dependent': 3, u'governorGloss': u'Gogh', u'governor': 4,
         u'dependentGloss': u'van'},
        {u'dep': u'nsubj', u'dependent': 4, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'Gogh'},
        {u'dep': u'cop', u'dependent': 5, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'was'},
        {u'dep': u'det', u'dependent': 6, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'a'},
        {u'dep': u'amod', u'dependent': 7, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'Dutch'},
        {u'dep': u'compound', u'dependent': 8, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'Post-Impressionist'},
        {u'dep': u'nsubj', u'dependent': 10, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'who'},
        {u'dep': u'cop', u'dependent': 11, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'is'},
        {u'dep': u'case', u'dependent': 12, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'among'},
        {u'dep': u'det', u'dependent': 13, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'the'},
        {u'dep': u'advmod', u'dependent': 14, u'governorGloss': u'famous', u'governor': 15,
         u'dependentGloss': u'most'},
        {u'dep': u'amod', u'dependent': 15, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'famous'},
        {u'dep': u'cc', u'dependent': 16, u'governorGloss': u'famous', u'governor': 15,
         u'dependentGloss': u'and'},
        {u'dep': u'conj', u'dependent': 17, u'governorGloss': u'famous', u'governor': 15,
         u'dependentGloss': u'influential'},
        {u'dep': u'acl:relcl', u'dependent': 18, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'figures'},
        {u'dep': u'case', u'dependent': 19, u'governorGloss': u'history', u'governor': 21,
         u'dependentGloss': u'in'},
        {u'dep': u'det', u'dependent': 20, u'governorGloss': u'history', u'governor': 21,
         u'dependentGloss': u'the'},
        {u'dep': u'nmod', u'dependent': 21, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'history'},
        {u'dep': u'case', u'dependent': 22, u'governorGloss': u'art', u'governor': 24,
         u'dependentGloss': u'of'},
        {u'dep': u'amod', u'dependent': 23, u'governorGloss': u'art', u'governor': 24,
         u'dependentGloss': u'Western'},
        {u'dep': u'nmod', u'dependent': 24, u'governorGloss': u'history', u'governor': 21,
         u'dependentGloss': u'art'},
        {u'dep': u'punct', u'dependent': 25, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'.'}],
    u'index': 0,
    u'tokens': [
        {u'index': 1, u'word': u'Vincent', u'lemma': u'Vincent', u'after': u' ', u'pos': u'NNP',
         u'characterOffsetEnd': 7, u'characterOffsetBegin': 0, u'originalText': u'Vincent',
         u'ner': u'PERSON', u'before': u''},
        {u'index': 2, u'word': u'Willem', u'lemma': u'Willem', u'after': u' ', u'pos': u'NNP',
         u'characterOffsetEnd': 14, u'characterOffsetBegin': 8, u'originalText': u'Willem',
         u'ner': u'PERSON', u'before': u' '},
        {u'index': 3, u'word': u'van', u'lemma': u'van', u'after': u' ', u'pos': u'NNP',
         u'characterOffsetEnd': 18, u'characterOffsetBegin': 15, u'originalText': u'van',
         u'ner': u'PERSON', u'before': u' '},
        {u'index': 4, u'word': u'Gogh', u'lemma': u'Gogh', u'after': u' ', u'pos': u'NNP',
         u'characterOffsetEnd': 23, u'characterOffsetBegin': 19, u'originalText': u'Gogh',
         u'ner': u'PERSON', u'before': u' '},
        {u'index': 5, u'word': u'was', u'lemma': u'be', u'after': u' ', u'pos': u'VBD',
         u'characterOffsetEnd': 27, u'characterOffsetBegin': 24, u'originalText': u'was',
         u'ner': u'O', u'before': u' '},
        {u'index': 6, u'word': u'a', u'lemma': u'a', u'after': u' ', u'pos': u'DT',
         u'characterOffsetEnd': 29, u'characterOffsetBegin': 28,
         u'originalText': u'a', u'ner': u'O', u'before': u' '},
        {u'index': 7, u'word': u'Dutch', u'lemma': u'dutch', u'after': u' ', u'pos': u'JJ',
         u'characterOffsetEnd': 35, u'characterOffsetBegin': 30, u'originalText': u'Dutch',
         u'ner': u'MISC', u'before': u' '},
        {u'index': 8, u'word': u'Post-Impressionist', u'lemma': u'post-impressionist',
         u'after': u' ',
         u'pos': u'NN', u'characterOffsetEnd': 54, u'characterOffsetBegin': 36,
         u'originalText': u'Post-Impressionist', u'ner': u'O', u'before': u' '},
        {u'index': 9, u'word': u'painter', u'lemma': u'painter', u'after': u' ', u'pos': u'NN',
         u'characterOffsetEnd': 62, u'characterOffsetBegin': 55, u'originalText': u'painter',
         u'ner': u'O', u'before': u' '},
        {u'index': 10, u'word': u'who', u'lemma': u'who', u'after': u' ', u'pos': u'WP',
         u'characterOffsetEnd': 66, u'characterOffsetBegin': 63, u'originalText': u'who',
         u'ner': u'O',
         u'before': u' '},
        {u'index': 11, u'word': u'is', u'lemma': u'be', u'after': u' ', u'pos': u'VBZ',
         u'characterOffsetEnd': 69, u'characterOffsetBegin': 67, u'originalText': u'is',
         u'ner': u'O',
         u'before': u' '},
        {u'index': 12, u'word': u'among', u'lemma': u'among', u'after': u' ', u'pos': u'IN',
         u'characterOffsetEnd': 75, u'characterOffsetBegin': 70, u'originalText': u'among',
         u'ner': u'O', u'before': u' '},
        {u'index': 13, u'word': u'the', u'lemma': u'the', u'after': u' ', u'pos': u'DT',
         u'characterOffsetEnd': 79, u'characterOffsetBegin': 76, u'originalText': u'the',
         u'ner': u'O',
         u'before': u' '},
        {u'index': 14, u'word': u'most', u'lemma': u'most', u'after': u' ', u'pos': u'RBS',
         u'characterOffsetEnd': 84, u'characterOffsetBegin': 80, u'originalText': u'most',
         u'ner': u'O',
         u'before': u' '},
        {u'index': 15, u'word': u'famous', u'lemma': u'famous', u'after': u' ', u'pos': u'JJ',
         u'characterOffsetEnd': 91, u'characterOffsetBegin': 85, u'originalText': u'famous',
         u'ner': u'O', u'before': u' '},
        {u'index': 16, u'word': u'and', u'lemma': u'and', u'after': u' ', u'pos': u'CC',
         u'characterOffsetEnd': 95, u'characterOffsetBegin': 92, u'originalText': u'and',
         u'ner': u'O',
         u'before': u' '},
        {u'index': 17, u'word': u'influential', u'lemma': u'influential', u'after': u' ',
         u'pos': u'JJ',
         u'characterOffsetEnd': 107, u'characterOffsetBegin': 96, u'originalText': u'influential',
         u'ner': u'O', u'before': u' '},
        {u'index': 18, u'word': u'figures', u'lemma': u'figure', u'after': u' ', u'pos': u'NNS',
         u'characterOffsetEnd': 115, u'characterOffsetBegin': 108, u'originalText': u'figures',
         u'ner': u'O', u'before': u' '},
        {u'index': 19, u'word': u'in', u'lemma': u'in', u'after': u' ', u'pos': u'IN',
         u'characterOffsetEnd': 118, u'characterOffsetBegin': 116, u'originalText': u'in',
         u'ner': u'O',
         u'before': u' '},
        {u'index': 20, u'word': u'the', u'lemma': u'the', u'after': u' ', u'pos': u'DT',
         u'characterOffsetEnd': 122, u'characterOffsetBegin': 119, u'originalText': u'the',
         u'ner': u'O', u'before': u' '},
        {u'index': 21, u'word': u'history', u'lemma': u'history', u'after': u' ', u'pos': u'NN',
         u'characterOffsetEnd': 130, u'characterOffsetBegin': 123, u'originalText': u'history',
         u'ner': u'O', u'before': u' '},
        {u'index': 22, u'word': u'of', u'lemma': u'of', u'after': u' ', u'pos': u'IN',
         u'characterOffsetEnd': 133, u'characterOffsetBegin': 131, u'originalText': u'of',
         u'ner': u'O', u'before': u' '},
        {u'index': 23, u'word': u'Western', u'lemma': u'western', u'after': u' ', u'pos': u'JJ',
         u'characterOffsetEnd': 141, u'characterOffsetBegin': 134, u'originalText': u'Western',
         u'ner': u'MISC', u'before': u' '},
        {u'index': 24, u'word': u'art', u'lemma': u'art', u'after': u'', u'pos': u'NN',
         u'characterOffsetEnd': 145, u'characterOffsetBegin': 142, u'originalText': u'art',
         u'ner': u'O', u'before': u' '},
        {u'index': 25, u'word': u'.', u'lemma': u'.', u'after': u'\n ', u'pos': u'.',
         u'characterOffsetEnd': 146, u'characterOffsetBegin': 145, u'originalText': u'.',
         u'ner': u'O', u'before': u''}],
    u'enhancedPlusPlusDependencies': [
        {u'dep': u'ROOT', u'dependent': 9, u'governorGloss': u'ROOT', u'governor': 0,
         u'dependentGloss': u'painter'},
        {u'dep': u'compound', u'dependent': 1, u'governorGloss': u'Gogh', u'governor': 4,
         u'dependentGloss': u'Vincent'},
        {u'dep': u'compound', u'dependent': 2, u'governorGloss': u'Gogh', u'governor': 4,
         u'dependentGloss': u'Willem'},
        {u'dep': u'compound', u'dependent': 3, u'governorGloss': u'Gogh', u'governor': 4,
         u'dependentGloss': u'van'},
        {u'dep': u'nsubj', u'dependent': 4, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'Gogh'},
        {u'dep': u'cop', u'dependent': 5, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'was'},
        {u'dep': u'det', u'dependent': 6, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'a'},
        {u'dep': u'amod', u'dependent': 7, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'Dutch'},
        {u'dep': u'compound', u'dependent': 8, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'Post-Impressionist'},
        {u'dep': u'nsubj', u'dependent': 9, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'painter'},
        {u'dep': u'ref', u'dependent': 10, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'who'},
        {u'dep': u'cop', u'dependent': 11, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'is'},
        {u'dep': u'case', u'dependent': 12, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'among'},
        {u'dep': u'det', u'dependent': 13, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'the'},
        {u'dep': u'advmod', u'dependent': 14, u'governorGloss': u'famous', u'governor': 15,
         u'dependentGloss': u'most'},
        {u'dep': u'amod', u'dependent': 15, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'famous'},
        {u'dep': u'cc', u'dependent': 16, u'governorGloss': u'famous', u'governor': 15,
         u'dependentGloss': u'and'},
        {u'dep': u'conj:and', u'dependent': 17, u'governorGloss': u'famous', u'governor': 15,
         u'dependentGloss': u'influential'},
        {u'dep': u'amod', u'dependent': 17, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'influential'},
        {u'dep': u'acl:relcl', u'dependent': 18, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'figures'},
        {u'dep': u'case', u'dependent': 19, u'governorGloss': u'history', u'governor': 21,
         u'dependentGloss': u'in'},
        {u'dep': u'det', u'dependent': 20, u'governorGloss': u'history', u'governor': 21,
         u'dependentGloss': u'the'},
        {u'dep': u'nmod:in', u'dependent': 21, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'history'},
        {u'dep': u'case', u'dependent': 22, u'governorGloss': u'art', u'governor': 24,
         u'dependentGloss': u'of'},
        {u'dep': u'amod', u'dependent': 23, u'governorGloss': u'art', u'governor': 24,
         u'dependentGloss': u'Western'},
        {u'dep': u'nmod:of', u'dependent': 24, u'governorGloss': u'history', u'governor': 21,
         u'dependentGloss': u'art'},
        {u'dep': u'punct', u'dependent': 25, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'.'}],
    u'enhancedDependencies': [
        {u'dep': u'ROOT', u'dependent': 9, u'governorGloss': u'ROOT', u'governor': 0,
         u'dependentGloss': u'painter'},
        {u'dep': u'compound', u'dependent': 1, u'governorGloss': u'Gogh', u'governor': 4,
         u'dependentGloss': u'Vincent'},
        {u'dep': u'compound', u'dependent': 2, u'governorGloss': u'Gogh', u'governor': 4,
         u'dependentGloss': u'Willem'},
        {u'dep': u'compound', u'dependent': 3, u'governorGloss': u'Gogh', u'governor': 4,
         u'dependentGloss': u'van'},
        {u'dep': u'nsubj', u'dependent': 4, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'Gogh'},
        {u'dep': u'cop', u'dependent': 5, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'was'},
        {u'dep': u'det', u'dependent': 6, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'a'},
        {u'dep': u'amod', u'dependent': 7, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'Dutch'},
        {u'dep': u'compound', u'dependent': 8, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'Post-Impressionist'},
        {u'dep': u'nsubj', u'dependent': 9, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'painter'},
        {u'dep': u'ref', u'dependent': 10, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'who'},
        {u'dep': u'cop', u'dependent': 11, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'is'},
        {u'dep': u'case', u'dependent': 12, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'among'},
        {u'dep': u'det', u'dependent': 13, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'the'},
        {u'dep': u'advmod', u'dependent': 14, u'governorGloss': u'famous', u'governor': 15,
         u'dependentGloss': u'most'},
        {u'dep': u'amod', u'dependent': 15, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'famous'},
        {u'dep': u'cc', u'dependent': 16, u'governorGloss': u'famous', u'governor': 15,
         u'dependentGloss': u'and'},
        {u'dep': u'conj:and', u'dependent': 17, u'governorGloss': u'famous', u'governor': 15,
         u'dependentGloss': u'influential'},
        {u'dep': u'amod', u'dependent': 17, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'influential'},
        {u'dep': u'acl:relcl', u'dependent': 18, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'figures'},
        {u'dep': u'case', u'dependent': 19, u'governorGloss': u'history', u'governor': 21,
         u'dependentGloss': u'in'},
        {u'dep': u'det', u'dependent': 20, u'governorGloss': u'history', u'governor': 21,
         u'dependentGloss': u'the'},
        {u'dep': u'nmod:in', u'dependent': 21, u'governorGloss': u'figures', u'governor': 18,
         u'dependentGloss': u'history'},
        {u'dep': u'case', u'dependent': 22, u'governorGloss': u'art', u'governor': 24,
         u'dependentGloss': u'of'},
        {u'dep': u'amod', u'dependent': 23, u'governorGloss': u'art', u'governor': 24,
         u'dependentGloss': u'Western'},
        {u'dep': u'nmod:of', u'dependent': 24, u'governorGloss': u'history', u'governor': 21,
         u'dependentGloss': u'art'},
        {u'dep': u'punct', u'dependent': 25, u'governorGloss': u'painter', u'governor': 9,
         u'dependentGloss': u'.'}]}

conll_plaintext = """Pierre  NNP     2       NMOD
Vinken  NNP     8       SUB
,       ,       2       P
61      CD      5       NMOD
years   NNS     6       AMOD
old     JJ      2       NMOD
,       ,       2       P
will    MD      0       ROOT
join    VB      8       VC
the     DT      11      NMOD
board   NN      9       OBJ
as      IN      9       VMOD
a       DT      15      NMOD
nonexecutive    JJ      15      NMOD
director        NN      12      PMOD
Nov.    NNP     9       VMOD
29      CD      16      NMOD
.       .       9       VMOD
"""

# noinspection PyCompatibility
conll_10 = (u'1\tVincent\tVincent\tNNP\tNNP\t\t4\tcompound\t_\t_\n'
            u'2\tWillem\tWillem\tNNP\tNNP\t\t4\tcompound\t_\t_\n'
            u'3\tvan\tvan\tNNP\tNNP\t\t4\tcompound\t_\t_\n'
            u'4\tGogh\tGogh\tNNP\tNNP\t\t9\tnsubj\t_\t_\n'
            u'5\twas\tbe\tVBD\tVBD\t\t9\tcop\t_\t_\n'
            u'6\ta\ta\tDT\tDT\t\t9\tdet\t_\t_\n'
            u'7\tDutch\tdutch\tJJ\tJJ\t\t9\tamod\t_\t_\n'
            u'8\tPost-Impressionist\tpost-impressionist\tNN\tNN\t\t9\tcompound\t_\t_\n'
            u'9\tpainter\tpainter\tNN\tNN\t\t0\tROOT\t_\t_\n'
            u'10\twho\twho\tWP\tWP\t\t18\tnsubj\t_\t_\n'
            u'11\tis\tbe\tVBZ\tVBZ\t\t18\tcop\t_\t_\n'
            u'12\tamong\tamong\tIN\tIN\t\t18\tcase\t_\t_\n'
            u'13\tthe\tthe\tDT\tDT\t\t18\tdet\t_\t_\n'
            u'14\tmost\tmost\tRBS\tRBS\t\t15\tadvmod\t_\t_\n'
            u'15\tfamous\tfamous\tJJ\tJJ\t\t18\tamod\t_\t_\n'
            u'16\tand\tand\tCC\tCC\t\t15\tcc\t_\t_\n'
            u'17\tinfluential\tinfluential\tJJ\tJJ\t\t15\tconj\t_\t_\n'
            u'18\tfigures\tfigure\tNNS\tNNS\t\t9\tacl:relcl\t_\t_\n'
            u'19\tin\tin\tIN\tIN\t\t21\tcase\t_\t_\n'
            u'20\tthe\tthe\tDT\tDT\t\t21\tdet\t_\t_\n'
            u'21\thistory\thistory\tNN\tNN\t\t18\tnmod\t_\t_\n'
            u'22\tof\tof\tIN\tIN\t\t24\tcase\t_\t_\n'
            u'23\tWestern\twestern\tJJ\tJJ\t\t24\tamod\t_\t_\n'
            u'24\tart\tart\tNN\tNN\t\t21\tnmod\t_\t_\n'
            u'25\t.\t.\t.\t.\t\t9\tpunct\t_\t_\n')

# noinspection PyCompatibility
dep_graph_nodes = {
    0: {u'ctag': u'TOP', u'head': None, u'word': None, u'deps': {u'ROOT': [9]}, u'lemma': None,
        u'tag': u'TOP', u'rel': None, u'address': 0, u'feats': None},
    1: {u'ctag': u'NNP', u'head': 4, u'deps': {}, u'tag': u'NNP', u'address': 1,
        u'word': u'Vincent', u'lemma': u'Vincent', u'rel': u'compound', u'feats': u''},
    2: {u'ctag': u'NNP', u'head': 4, u'deps': {}, u'tag': u'NNP', u'address': 2, u'word': u'Willem',
        u'lemma': u'Willem', u'rel': u'compound', u'feats': u''},
    3: {u'ctag': u'NNP', u'head': 4, u'deps': {}, u'tag': u'NNP', u'address': 3, u'word': u'van',
        u'lemma': u'van', u'rel': u'compound', u'feats': u''},
    4: {u'ctag': u'NNP', u'head': 9, u'deps': {u'compound': [1, 2, 3]}, u'tag': u'NNP',
        u'address': 4, u'word': u'Gogh', u'lemma': u'Gogh', u'rel': u'nsubj', u'feats': u''},
    5: {u'ctag': u'VBD', u'head': 9, u'deps': {}, u'tag': u'VBD', u'address': 5, u'word': u'was',
        u'lemma': u'be', u'rel': u'cop', u'feats': u''},
    6: {u'ctag': u'DT', u'head': 9, u'deps': {}, u'tag': u'DT', u'address': 6, u'word': u'a',
        u'lemma': u'a', u'rel': u'det', u'feats': u''},
    7: {u'ctag': u'JJ', u'head': 9, u'deps': {}, u'tag': u'JJ', u'address': 7, u'word': u'Dutch',
        u'lemma': u'dutch', u'rel': u'amod', u'feats': u''},
    8: {u'ctag': u'NN', u'head': 9, u'deps': {}, u'tag': u'NN', u'address': 8,
        u'word': u'Post-Impressionist', u'lemma': u'post-impressionist', u'rel': u'compound',
        u'feats': u''},
    9: {u'ctag': u'NN', u'head': 0,
        u'deps': {u'cop': [5], u'nsubj': [4], u'det': [6], u'amod': [7],
                  u'punct': [25], u'acl:relcl': [18], u'compound': [8]},
        u'tag': u'NN', u'address': 9, u'word': u'painter', u'lemma': u'painter',
        u'rel': u'ROOT', u'feats': u''},
    10: {u'ctag': u'WP', u'head': 18, u'deps': {}, u'tag': u'WP', u'address': 10, u'word': u'who',
         u'lemma': u'who', u'rel': u'nsubj', u'feats': u''},
    11: {u'ctag': u'VBZ', u'head': 18, u'deps': {}, u'tag': u'VBZ', u'address': 11, u'word': u'is',
         u'lemma': u'be', u'rel': u'cop', u'feats': u''},
    12: {u'ctag': u'IN', u'head': 18, u'deps': {}, u'tag': u'IN', u'address': 12, u'word': u'among',
         u'lemma': u'among', u'rel': u'case', u'feats': u''},
    13: {u'ctag': u'DT', u'head': 18, u'deps': {}, u'tag': u'DT', u'address': 13, u'word': u'the',
         u'lemma': u'the', u'rel': u'det', u'feats': u''},
    14: {u'ctag': u'RBS', u'head': 15, u'deps': {}, u'tag': u'RBS', u'address': 14,
         u'word': u'most', u'lemma': u'most', u'rel': u'advmod', u'feats': u''},
    15: {u'ctag': u'JJ', u'head': 18, u'deps': {u'cc': [16], u'conj': [17], u'advmod': [14]},
         u'tag': u'JJ', u'address': 15, u'word': u'famous', u'lemma': u'famous', u'rel': u'amod',
         u'feats': u''},
    16: {u'ctag': u'CC', u'head': 15, u'deps': {}, u'tag': u'CC', u'address': 16, u'word': u'and',
         u'lemma': u'and', u'rel': u'cc', u'feats': u''},
    17: {u'ctag': u'JJ', u'head': 15, u'deps': {}, u'tag': u'JJ', u'address': 17,
         u'word': u'influential', u'lemma': u'influential', u'rel': u'conj', u'feats': u''},
    18: {u'ctag': u'NNS', u'head': 9,
         u'deps': {u'case': [12], u'cop': [11], u'nsubj': [10], u'det': [13], u'nmod': [21],
                   u'amod': [15]}, u'tag': u'NNS', u'address': 18, u'word': u'figures',
         u'lemma': u'figure', u'rel': u'acl:relcl', u'feats': u''},
    19: {u'ctag': u'IN', u'head': 21, u'deps': {}, u'tag': u'IN', u'address': 19, u'word': u'in',
         u'lemma': u'in', u'rel': u'case', u'feats': u''},
    20: {u'ctag': u'DT', u'head': 21, u'deps': {}, u'tag': u'DT', u'address': 20, u'word': u'the',
         u'lemma': u'the', u'rel': u'det', u'feats': u''},
    21: {u'ctag': u'NN', u'head': 18, u'deps': {u'case': [19], u'det': [20], u'nmod': [24]},
         u'tag': u'NN', u'address': 21, u'word': u'history', u'lemma': u'history', u'rel': u'nmod',
         u'feats': u''},
    22: {u'ctag': u'IN', u'head': 24, u'deps': {}, u'tag': u'IN', u'address': 22, u'word': u'of',
         u'lemma': u'of', u'rel': u'case', u'feats': u''},
    23: {u'ctag': u'JJ', u'head': 24, u'deps': {}, u'tag': u'JJ', u'address': 23,
         u'word': u'Western', u'lemma': u'western', u'rel': u'amod', u'feats': u''},
    24: {u'ctag': u'NN', u'head': 21, u'deps': {u'case': [22], u'amod': [23]}, u'tag': u'NN',
         u'address': 24, u'word': u'art', u'lemma': u'art', u'rel': u'nmod', u'feats': u''},
    25: {u'ctag': u'.', u'head': 9, u'deps': {}, u'tag': u'.', u'address': 25, u'word': u'.',
         u'lemma': u'.', u'rel': u'punct', u'feats': u''}}

dragnn_sent_text = """text: "John is eating pizza with a fork"
token {
  word: "John"
  start: 0
  end: 3
  head: 2
  tag: "attribute { name: \"Number\" value: \"Sing\" } attribute { name: \"fPOS\" value: \"PROPN++NNP\" } "
  category: ""
  label: "nsubj"
  break_level: NO_BREAK
}
token {
  word: "is"
  start: 5
  end: 6
  head: 2
  tag: "attribute { name: \"Mood\" value: \"Ind\" } attribute { name: \"Number\" value: \"Sing\" } attribute { name: \"Person\" value: \"3\" } attribute { name: \"Tense\" value: \"Pres\" } attribute { name: \"VerbForm\" value: \"Fin\" } attribute { name: \"fPOS\" value: \"AUX++VBZ\" } "
  category: ""
  label: "aux"
  break_level: SPACE_BREAK
}
token {
  word: "eating"
  start: 8
  end: 13
  tag: "attribute { name: \"Tense\" value: \"Pres\" } attribute { name: \"VerbForm\" value: \"Part\" } attribute { name: \"fPOS\" value: \"VERB++VBG\" } "
  category: ""
  label: "root"
  break_level: SPACE_BREAK
}
token {
  word: "pizza"
  start: 15
  end: 19
  head: 2
  tag: "attribute { name: \"Number\" value: \"Sing\" } attribute { name: \"fPOS\" value: \"NOUN++NN\" } "
  category: ""
  label: "obj"
  break_level: SPACE_BREAK
}
token {
  word: "with"
  start: 21
  end: 24
  head: 6
  tag: "attribute { name: \"fPOS\" value: \"ADP++IN\" } "
  category: ""
  label: "case"
  break_level: SPACE_BREAK
}
token {
  word: "a"
  start: 26
  end: 26
  head: 6
  tag: "attribute { name: \"Definite\" value: \"Ind\" } attribute { name: \"PronType\" value: \"Art\" } attribute { name: \"fPOS\" value: \"DET++DT\" } "
  category: ""
  label: "det"
  break_level: SPACE_BREAK
}
token {
  word: "fork"
  start: 28
  end: 31
  head: 2
  tag: "attribute { name: \"Number\" value: \"Sing\" } attribute { name: \"fPOS\" value: \"NOUN++NN\" } "
  category: ""
  label: "obl"
  break_level: SPACE_BREAK
}
"""


def test_stanford_nltk_parse():
    from nlp_util.stanford_nltk_nlp import ParsedSent
    from nltk.parse.dependencygraph import DependencyGraph
    from nltk.tree import Tree
    nltk_dep_graph = DependencyGraph(conll_plaintext)
    parsed_sent = ParsedSent(nltk_dep_graph)
    tagged_list = parsed_sent.tagged_list
    dep_list = parsed_sent.dep_list
    dep_tree = parsed_sent.get_dep_tree()
    pprint(tagged_list)
    pprint(dep_list)
    pprint(dep_tree)
    Tree.fromstring(dep_tree).draw()
    dep_tree = parsed_sent.get_dep_tree(8)
    Tree.fromstring(dep_tree).draw()


def test_stanford_corenlp_parse():
    from nlp_util.stanford_corenlp import ParsedSent
    from nltk.tree import Tree
    parsed_sent = ParsedSent(corenlp_sent)
    tagged_list = parsed_sent.tagged_list
    dep_list = parsed_sent.dep_list
    parsed_sent._leaf_func = (lambda x: tagged_list[x][0])
    dep_tree = parsed_sent.get_dep_tree()
    pprint(tagged_list)
    pprint(dep_list)
    pprint(dep_tree)
    Tree.fromstring(dep_tree).draw()


def test_feature_trees():
    from nlp_util.interface import get_feature_trees
    from nlp_util.interface import calc_tree_similarity
    t = '(S (NP (D a) (N dog)) (VP (V chased) (NP (D the) (N cat))))'
    s = '(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))'
    pprint(get_feature_trees(t))
    print(calc_tree_similarity(t, s))
    pass


if __name__ == '__main__':
    # import nlp_util.xxx

    # noinspection PyCompatibility
    # reload(nlp_util.xxx)
    # test()
    test_stanford_nltk_parse()

    pass
