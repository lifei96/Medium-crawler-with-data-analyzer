# -*- coding: utf-8 -*-

from util_graph import *


if __name__ == '__main__':
    get_comm_edge('./data/graph/community/graph_labeled_louvain.dat', './data/graph/community/graph_node2comm_level3.txt', './data/graph/community/comm_edge.csv')
