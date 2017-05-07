# -*- coding: utf-8 -*-

import os
import glob
import json


def get_nodes():
    nodes = set()
    current_path = os.getcwd()
    os.chdir('./data/Users')
    for filename in glob.glob('*.json'):
        nodes.add(filename[:-5])
    os.chdir(current_path)
    return nodes


def get_edges(username, nodes):
    edges = list()
    with open('./data/Users/' + username + '.json', 'r') as f:
        user = json.load(f)
    for node in user['following']:
        if node in nodes:
            edges.append(node)
    return edges


def get_graph(f):
    nodes = get_nodes()
    print "-----nodes"
    total = len(nodes)
    cnt = 0
    for node in nodes:
        edges = get_edges(node, nodes)
        output = [node] + edges
        f.write(' '.join(output) + '\n')
        cnt += 1
        print '%d/%d' % (cnt, total)


if __name__ == '__main__':
    with open('./data/graph/graph.dat', 'a') as f:
        get_graph(f)
