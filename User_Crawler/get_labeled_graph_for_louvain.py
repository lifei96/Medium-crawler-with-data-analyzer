# -*- coding: utf-8 -*-

from util_graph import *


if __name__ == '__main__':
    get_labeled_graph_for_louvain('./data/graph/graph.dat', './data/graph/graph_labeled_louvain.dat', './data/graph/nodes_hash_louvain.dat')
