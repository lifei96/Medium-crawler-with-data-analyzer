# -*- coding: utf-8 -*-

from util_graph import *


if __name__ == '__main__':
    get_comm('./data/graph/community/graph_node2comm_level3.txt', './data/graph/community/nodes_hash_louvain.dat', './data/graph/community/user2comm.csv', './data/graph/community/comm_size.csv')
