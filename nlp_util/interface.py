# coding: utf-8

"""
Utility Tools for Stanford CoreNLP Server
=========================================
Interfaces
"""

__author__ = "GE Ning <https://github.com/gening/>"
__copyright__ = "Copyright (C) 2017 GE Ning"
__license__ = "LGPL-3.0"
__version__ = "1.0"


class SentDependencyI(object):
    def __init__(self, dep_graph, root_index, make_tree=None, make_leaf=None):
        # graph
        self._dep_graph = dep_graph
        self._root_index = root_index
        self._node_num = len(dep_graph)
        # tree formatter
        self._tree_func = make_tree if hasattr(make_tree, '__call__') else _format_tree
        self._leaf_func = make_leaf if hasattr(make_leaf, '__call__') else _format_leaf
        # property
        self._dep_list = None

    @property
    def dep_list(self):
        if self._dep_list is None:
            self._dep_list = []
            for index, node in enumerate(self._dep_graph):
                if 'rel' in node:
                    rel = node['rel']
                    head_id = node['head']
                    # if root: head_id = id
                    if head_id == -1:
                        head_id = index
                        left_edge = 0
                        right_edge = self._node_num - 1
                    else:
                        left_edge = self.left_edge(head_id)
                        right_edge = self.right_edge(head_id)
                else:
                    rel = 'MISSING'
                    head_id = left_edge = right_edge = index
                self._dep_list.append((rel,  # dep relation name
                                       head_id,  # head index
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
            if self._root_index is None:
                return None
            else:
                index = self._root_index
        elif index < 0 or index >= self._node_num:
            raise ValueError('index out of range')
        graph_vertex_status = ['O'] * self._node_num
        if index == self._root_index:
            label = 'ROOT'
        else:
            label = 'S'
        return self._spanning_tree(graph_vertex_status, index, label)

    def _spanning_tree(self, visiting_array, node_index, node_label):
        visiting_array[node_index] = 'V'
        root = node_label  # dep_name
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
        return self._tree_func(root, [subtrees[i] for i in sorted(subtrees)])


def _format_tree(root_label, subtree_list):
    return '(' + root_label + (' ' + ' '.join(subtree_list) if subtree_list else '') + ')'
    # from nltk.tree import Tree
    # return Tree(root, subtree_list)


def _format_leaf(index):
    return str(index)
