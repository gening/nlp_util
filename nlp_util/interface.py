# coding: utf-8

"""
Interfaces of the package
=========================
Dependency graph class
Extract feature trees, and the similarity between trees. 
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"


class DependencyGraphI(object):
    def __init__(self, dep_graph=None, make_tree=None, make_leaf=None):
        # Considering that:
        # 1. almost every token has its head token,
        # 2. the order of tokens in the original text is very necessary,
        # 3. -1 as index has a different meaning in Python,
        # dep_graph is represented as a list similar to tagged_list, which index is 0-based
        # and the root is represented in the way that its head index = its index.
        # property
        self._dep_graph = dep_graph
        self._root_index = None
        self._dep_list = None
        # tree formatter
        self._tree_func = make_tree if hasattr(make_tree, '__call__') else _format_tree
        self._leaf_func = make_leaf if hasattr(make_leaf, '__call__') else _format_leaf

    @property
    def dep_graph(self):
        return self._dep_graph

    @dep_graph.setter
    def dep_graph(self, value):
        self._dep_graph = value

    def _add_dep_arc(self, dep_index, dep_rel, head_index):
        # When one mapped into two heads.
        # these relations are stored in the dep_graph[head_index]['deps']
        # dep_graph[dep_index]['head'] is only the nearest head_index.
        # Note:
        # only add arc, and cannot add new node

        # additional index protection
        if head_index is None or head_index == -1:
            head_index = dep_index

        # arc: from dep to head
        condition = False
        if 'head' not in self._dep_graph[dep_index]:
            # not exist
            condition = True
        else:
            # already exists and the nearest will be selected
            h = self._dep_graph[dep_index]['head']
            # additional protection: None, -1
            if h is not None and h != -1 and abs(head_index - dep_index) < abs(h - dep_index):
                condition = True
        if condition:
            self._dep_graph[dep_index]['rel'] = dep_rel
            self._dep_graph[dep_index]['head'] = head_index
            # to rebuild the dep list
            self._dep_list = None

        # arc: from head to sets of dep
        if head_index == dep_index:
            # root
            if self._root_index is None:
                self._root_index = dep_index
            elif dep_index < self._root_index:
                self._root_index = dep_index
        else:
            # not root
            self._dep_graph[head_index].setdefault(
                'deps', dict()).setdefault(
                dep_rel, list()).append(dep_index)

    @property
    def _node_num(self):
        return len(self._dep_graph)

    @property
    def root_index(self):
        if self._root_index is None:
            for index, node in enumerate(self._dep_graph):
                # root
                if node['head'] is None or node['head'] == -1 or node['head'] == index:
                    # the first root
                    self._root_index = index
                    break
        return self._root_index

    @root_index.setter
    def root_index(self, value):
        if value is not None and (value < 0 or value >= self._node_num):
            raise ValueError('index out of range')
        self._root_index = value

    @property
    def dep_list(self):
        if self._dep_list is None:
            self._dep_list = []
            for index, node in enumerate(self._dep_graph):
                if 'rel' in node:
                    rel = node['rel']
                    head_index = node['head']
                    if head_index is None or head_index == -1:
                        # additional index protection
                        head_index = index
                    left_edge = self.left_edge(head_index)
                    right_edge = self.right_edge(head_index)
                else:
                    rel = 'MISSING'
                    head_index = left_edge = right_edge = index
                self._dep_list.append((rel,  # dep relation name
                                       head_index,  # head index
                                       left_edge,  # start = left_edge
                                       right_edge  # end = right_edge + 1
                                       ))
        return self._dep_list

    def left_edge(self, index):
        if index < 0 or index >= self._node_num:
            raise ValueError('index out of range')
        left = index
        loop = True
        while loop:
            deps = self._dep_graph[left].get('deps', None)
            if deps:
                for dep_id_list in deps.values():
                    for dep_id in dep_id_list:
                        if dep_id < left:
                            left = dep_id
                        else:
                            loop = False
            else:
                loop = False
        return left

    def right_edge(self, index):
        if index < 0 or index >= self._node_num:
            raise ValueError('index out of range')
        right = index
        loop = True
        while loop:
            deps = self._dep_graph[right].get('deps', None)
            if deps:
                for dep_id_list in deps.values():
                    for dep_id in dep_id_list:
                        if dep_id > right:
                            right = dep_id
                        else:
                            loop = False
            else:
                loop = False
        return right

    def get_dep_tree(self, index=None):
        if index is None:
            if self.root_index is None:
                return None
            else:
                index = self.root_index
        elif index < 0 or index >= self._node_num:
            raise ValueError('index out of range')
        graph_vertex_status = ['O'] * self._node_num
        if index == self.root_index:
            label = 'ROOT'
        else:
            label = 'S'
        return self._spanning_tree(graph_vertex_status, index, label)

    def _spanning_tree(self, visiting_array, node_index, node_label):
        visiting_array[node_index] = 'V'
        root_label = node_label  # dep_name
        subtrees = dict()
        leaf = self._leaf_func(node_index)
        if 'deps' not in self._dep_graph[node_index]:
            subtrees[node_index] = leaf
        else:
            subtrees[node_index] = self._tree_func('^', [leaf])
            for dep_rel, dep_id_list in self._dep_graph[node_index]['deps'].items():
                for dep_id in dep_id_list:
                    if visiting_array[dep_id] == 'V':
                        # has already visited
                        continue
                    subtrees[dep_id] = self._spanning_tree(visiting_array, dep_id, dep_rel)
        return self._tree_func(root_label, [subtrees[i] for i in sorted(subtrees)])


def _format_tree(root_label, subtree_list):
    return '(' + root_label + (' ' + ' '.join(subtree_list) if subtree_list else '') + ')'
    # from nltk.tree import Tree
    # return Tree(root_label, subtree_list)


def _format_leaf(index):
    return str(index)


def get_feature_trees(tree_str, sorting=False):
    # For the definition of feature tree, please see:
    # http://disi.unitn.it/moschitti/Tree-Kernel.htm
    # http://papers.nips.cc/paper/2089-convolution-kernels-for-natural-language.pdf
    # A given tree will have a number of subtrees that is exponential in its size.

    # when importing a module, python will lookup sys.modules.
    # if the module has already been imported, python will skip the import statement.
    from collections import defaultdict
    from nltk.tree import Tree
    this_tree = Tree.fromstring(tree_str)
    # global variable
    # result: list(tuple) = [(address, tree), ...]
    results = []
    # index: dict(list), the index of a tree in results -> feet
    index = defaultdict(list)
    # inverted_index(倒排索引): dict(list), tail address -> the indices of trees
    inverted_index = defaultdict(list)

    # add tail to the existing trees via index
    def expand_trees(tree, address):
        if tree.height() < 2:
            pass
        elif tree.height() == 2:
            tree_element = tree
            results.append((address, tree_element))
            # install the tail to the applicable trees
            for ii in inverted_index[address]:
                existing_tree_address, existing_tree = results[ii]
                new_tree = existing_tree.copy(deep=True)
                # existing_tree_address: (0, 0)
                # address: (0, 0, 1)
                new_tree[address[len(existing_tree_address):]] = tree_element
                results.append((existing_tree_address, new_tree))
                # update index with other tails
                # no need to update index with its tails
                new_tree_pos = len(results) - 1
                for tail_address in index[ii]:
                    if tail_address != address:
                        index[new_tree_pos].append(tail_address)
                        inverted_index[tail_address].append(new_tree_pos)
        else:
            root = tree.label()
            children = [tree[ii].label() for ii in range(len(tree))]
            tree_element = Tree(root, children)
            results.append((address, tree_element))
            tree_pos = len(results) - 1
            # install the tail to the applicable trees
            for ii in inverted_index[address]:
                existing_tree_address, existing_tree = results[ii]
                new_tree = existing_tree.copy(deep=True)
                # existing_tree_address: (0, 0)
                # address: (0, 0, 1)
                new_tree[address[len(existing_tree_address):]] = tree_element
                results.append((existing_tree_address, new_tree))
                # update index with other tails
                new_tree_pos = len(results) - 1
                for tail_address in index[ii]:
                    if tail_address != address:
                        index[new_tree_pos].append(tail_address)
                        inverted_index[tail_address].append(new_tree_pos)
            # update index with its tails
            for ii in range(len(tree)):
                sub_tree_address = tuple(list(address) + [ii])
                for jj in range(tree_pos, len(results)):
                    index[jj].append(sub_tree_address)
                    inverted_index[sub_tree_address].append(jj)

    # Breadth-First-Search
    queue = [(this_tree, tuple())]  # (tree, root_address)
    while len(queue) > 0:
        this_tree, this_address = queue.pop(0)
        if isinstance(this_tree, Tree):
            expand_trees(this_tree, this_address)
            # decompose
            if this_tree.height() > 2:
                for sub_tree_index in range(len(this_tree)):
                    next_tree = this_tree[sub_tree_index]
                    next_address = tuple(list(this_address) + [sub_tree_index])
                    queue.append((next_tree, next_address))
    if sorting:
        results = sorted(results)
    return map(str, zip(*results)[1])


def calc_tree_similarity(tree_str1, tree_str2):
    if tree_str1 == tree_str2:
        return 1.00
    else:
        # make sure: similarity(s, t) == similarity(t, s)
        j = i = 0
        fea_set1 = get_feature_trees(tree_str1)
        fea_set2 = get_feature_trees(tree_str2)
        len1 = len(fea_set1)
        len2 = len(fea_set2)
        for fea in fea_set1:
            if fea in fea_set2:
                i += 1
        for fea in fea_set2:
            if fea in fea_set1:
                j += 1
        return 1.00 * (i + j) / (len1 - 1 + len2 - 1)
