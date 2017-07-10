# -*- coding: utf-8 -*-

from util_graph import *


if __name__ == '__main__':
    get_labeled_LSCC_for_paths('./data/graph/graph.dat', './data/graph/LSCC_labeled_paths.dat', './data/graph/nodes_hash_LSCC.dat')
