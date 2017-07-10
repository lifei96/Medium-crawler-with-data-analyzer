# -*- coding: utf-8 -*-

import snap
import pandas as pd
import os
import json
from operator import *


eps = 1e-10


def load_graph(file_path):
    H = snap.TStrIntSH()
    Graph = snap.LoadConnListStr(snap.PNGraph, file_path, H)
    print "-----graph loaded"
    return Graph, H


def get_labeled_graph(file_path, output_path_graph, output_path_hash):
    Graph, H = load_graph(file_path)
    with open(output_path_graph, 'w') as f:
        print '-----clear'
    with open(output_path_hash, 'w') as f:
        print '-----clear'
    f_graph = open(output_path_graph, 'a')
    f_hash = open(output_path_hash, 'a')
    for NI in Graph.Nodes():
        ID = NI.GetId()
        f_hash.write('%d %s\n' % (ID, H.GetKey(ID)))
        f_graph.write('%d' % ID)
        for des in NI.GetOutEdges():
            f_graph.write(' %d' % des)
        f_graph.write('\n')
        print ID


def get_labeled_graph_for_CC(file_path, output_path_graph, output_path_hash):
    Graph, H = load_graph(file_path)
    with open(output_path_graph, 'w') as f:
        print '-----clear'
    with open(output_path_hash, 'w') as f:
        print '-----clear'
    f_graph = open(output_path_graph, 'a')
    f_hash = open(output_path_hash, 'a')
    for NI in Graph.Nodes():
        ID = NI.GetId()
        f_hash.write('%d %s\n' % (ID, H.GetKey(ID)))
        f_graph.write('%d %d' % (ID, NI.GetOutDeg()))
        for des in NI.GetOutEdges():
            f_graph.write(' %d' % des)
        f_graph.write('\n')
        print ID


def get_labeled_graph_for_louvain(file_path, output_path_graph, output_path_hash):
    Graph, H = load_graph(file_path)
    with open(output_path_graph, 'w') as f:
        print '-----clear'
    with open(output_path_hash, 'w') as f:
        print '-----clear'
    f_graph = open(output_path_graph, 'a')
    f_hash = open(output_path_hash, 'a')
    for NI in Graph.Nodes():
        ID = NI.GetId()
        f_hash.write('%d %s\n' % (ID, H.GetKey(ID)))
        for des in NI.GetOutEdges():
            f_graph.write('%d %d\n' % (ID, des))
        print ID


def get_labeled_LSCC_for_paths(file_path, output_path_LSCC, output_path_hash):
    Graph, H = load_graph(file_path)
    MxScc = snap.GetMxScc(Graph)
    with open(output_path_LSCC, 'w') as f:
        print '-----clear'
    with open(output_path_hash, 'w') as f:
        print '-----clear'
    f_graph = open(output_path_LSCC, 'a')
    f_hash = open(output_path_hash, 'a')
    for NI in MxScc.Nodes():
        ID = NI.GetId()
        f_hash.write('%d %s\n' % (ID, H.GetKey(ID)))
        for des in NI.GetOutEdges():
            f_graph.write('%d %d\n' % (ID, des))
        print ID


def merge_CC_result(path_CC, path_hash, output_path):
    CC = dict()
    dataset = list()
    with open(path_CC, 'r') as f:
        raw_data = f.read().split('\n')
        for line in raw_data:
            if line != '':
                ID, cc = map(eval, line.split())
                CC[ID] = cc
    with open(path_hash, 'r') as f:
        raw_data = f.read().split('\n')
        for line in raw_data:
            if line != '':
                ID, username = line.split()
                ID = eval(ID)
                dataset.append({'username': username, 'CC': CC[ID]})
    dataset = pd.DataFrame(dataset)
    dataset = dataset[['username', 'CC']]
    dataset.to_csv(output_path, index=False, encoding='utf-8')


def get_graph_info(file_path, output_path):
    Graph, H = load_graph(file_path)
    snap.PrintInfo(Graph, 'Python type PNGraph', output_path, False)


def graph_cleaning(file_path):
    Graph, H = load_graph(file_path)
    Graph = snap.GetMxWcc(Graph)
    snap.DelSelfEdges(Graph)
    nodes_set = set()
    for NI in Graph.Nodes():
        nodes_set.add(NI.GetId())
    with open(file_path, 'r') as f:
        raw_list = f.read().split('\n')
        edges_list = [edge_str.split() for edge_str in raw_list]
    with open(file_path, 'w') as f:
        print '-----clear'
    with open(file_path, 'a') as f:
        for edge in edges_list:
            if len(edge) == 0:
                continue
            if H.GetKeyId(edge[0]) not in nodes_set:
                continue
            edge_cleaned = list()
            for node in edge:
                if H.GetKeyId(node) in nodes_set:
                    edge_cleaned.append(node)
            f.write(' '.join(edge_cleaned) + '\n')


def get_pagerank(file_path, output_path):
    Graph, H = load_graph(file_path)
    PRankH = snap.TIntFltH()
    snap.GetPageRank(Graph, PRankH)
    pr_list = list()
    for ID in PRankH:
        pr_list.append({'username': H.GetKey(ID), 'PR': PRankH[ID]})
    dataset = pd.DataFrame(pr_list)
    dataset = dataset[['username', 'PR']]
    dataset.to_csv(output_path, index=False, encoding='utf-8')


def get_degree(file_path, output_path):
    Graph, H = load_graph(file_path)
    InDegV = snap.TIntPrV()
    snap.GetNodeInDegV(Graph, InDegV)
    InDeg_set = dict()
    for item in InDegV:
        username = H.GetKey(item.GetVal1())
        InDeg = item.GetVal2()
        InDeg_set[username] = InDeg
    OutDegV = snap.TIntPrV()
    snap.GetNodeOutDegV(Graph, OutDegV)
    OutDeg_set = dict()
    for item in OutDegV:
        username = H.GetKey(item.GetVal1())
        OutDeg = item.GetVal2()
        OutDeg_set[username] = OutDeg
    dataset = list()
    tot = len(InDeg_set)
    num = 0
    for username in InDeg_set:
        user_degree = dict()
        user_degree['username'] = username
        user_degree['in_degree'] = InDeg_set[username]
        user_degree['out_degree'] = OutDeg_set[username]
        profile_path = './data/Users/%s.json' % username
        if not os.path.exists(profile_path):
            continue
        with open(profile_path, 'r') as f:
            profile = json.load(f)
        if 'socialStats' in profile['profile']['user']:
            user_degree['in_degree'] = max(user_degree['in_degree'], profile['profile']['user']['socialStats']['usersFollowedByCount'])
            user_degree['out_degree'] = max(user_degree['out_degree'], profile['profile']['user']['socialStats']['usersFollowedCount'])
        in_set = set(profile['followers'])
        out_set = set(profile['following'])
        user_degree['in_degree'] = max(user_degree['in_degree'], len(in_set))
        user_degree['out_degree'] = max(user_degree['out_degree'], len(out_set))
        if user_degree['out_degree'] == 0:
            user_degree['balance'] = float(user_degree['in_degree']) / eps
        else:
            user_degree['balance'] = float(user_degree['in_degree']) / float(user_degree['out_degree'])
        bi = 0
        for out_username in out_set:
            if out_username in in_set:
                bi += 1
        if user_degree['out_degree'] == 0:
            user_degree['reciprocity'] = float(bi) / eps
        else:
            user_degree['reciprocity'] = float(bi) / float(user_degree['out_degree'])
        dataset.append(user_degree)
        num += 1
        print '%d/%d' % (num, tot)
    dataset = pd.DataFrame(dataset)
    dataset = dataset[['username', 'in_degree', 'out_degree', 'balance', 'reciprocity']]
    dataset.to_csv(output_path, index=False, encoding='utf-8')


def get_CC(file_path, output_path):
    Graph, H = load_graph(file_path)
    NIdCCfH = snap.TIntFltH()
    snap.GetNodeClustCf(Graph, NIdCCfH)
    dataset = list()
    for ID in NIdCCfH:
        CC = dict()
        CC['username'] = H.GetKey(ID)
        CC['CC'] = NIdCCfH[ID]
        dataset.append(CC)
    dataset = pd.DataFrame(dataset)
    dataset = dataset[['username', 'CC']]
    dataset.to_csv(output_path, index=False, encoding='utf-8')


def get_SCC(file_path, output_path):
    Graph, H = load_graph(file_path)
    ComponentDist = snap.TIntPrV()
    snap.GetSccSzCnt(Graph, ComponentDist)
    dataset = list()
    for comp in ComponentDist:
        scc = dict()
        scc['size'] = comp.GetVal1()
        scc['freq'] = comp.GetVal2()
        dataset.append(scc)
    dataset = pd.DataFrame(dataset)
    dataset = dataset[['size', 'freq']]
    dataset.sort('size', ascending=0, inplace=True)
    dataset.to_csv(output_path, index=False, encoding='utf-8')


def get_shortest_path(file_path, output_path):
    Graph, H = load_graph(file_path)
    path_distr = dict()
    MxScc = snap.GetMxScc(Graph)
    tot = MxScc.GetNodes()
    cnt = 0
    for NI in MxScc.Nodes():
        NIdToDistH = snap.TIntH()
        shortestPath = snap.GetShortPath(MxScc, NI.GetId(), NIdToDistH, True)
        for ID in NIdToDistH:
            dist = NIdToDistH[ID]
            if dist in path_distr:
                path_distr[dist] += 1
            else:
                path_distr[dist] = 1
        cnt += 1
        print '%d/%d' % (cnt, tot)
    dataset = list()
    for dist in path_distr:
        distr = dict()
        distr['dist'] = dist
        distr['freq'] = path_distr[dist]
        dataset.append(distr)
    dataset = pd.DataFrame(dataset)
    dataset = dataset[['dist', 'freq']]
    dataset.sort('dist', ascending=1, inplace=True)
    dataset.to_csv(output_path, index=False, encoding='utf-8')


def get_comm(node2comm_path, hash_path, output_path_user2comm, output_path_comm_size):
    with open(node2comm_path, 'r') as f:
        raw_data = f.read().split('\n')
    ID2comm = dict()
    for line in raw_data:
        if line == '':
            continue
        ID, comm_no = map(eval, line.split())
        ID2comm[ID] = comm_no
    user2comm = list()
    comm = dict()
    with open(hash_path, 'r') as f:
        raw_data = f.read().split('\n')
        for line in raw_data:
            if line != '':
                ID, username = line.split()
                ID = eval(ID)
                user2comm.append({'username': username, 'comm': ID2comm[ID]})
                if ID2comm[ID] in comm:
                    comm[ID2comm[ID]] += 1
                else:
                    comm[ID2comm[ID]] = 1
    tot = len(user2comm)
    comm_size = list()
    for comm_no in comm:
        comm_size.append({'comm': comm_no, 'size': comm[comm_no], 'perc': 1.0 * comm[comm_no] / tot})
    user2comm = pd.DataFrame(user2comm)
    user2comm = user2comm[['username', 'comm']]
    user2comm.to_csv(output_path_user2comm, index=False, encoding='utf-8')
    comm_size = pd.DataFrame(comm_size)
    comm_size = comm_size[['comm', 'size', 'perc']]
    comm_size.sort('size', ascending=0, inplace=True)
    comm_size.to_csv(output_path_comm_size, index=False, encoding='utf-8')


def get_comm_edge(graph_path, node2comm_path, output_path):
    comm_intra = dict()
    comm_inter = dict()
    node2comm = dict()
    comm_size = dict()
    with open(node2comm_path, 'r') as f:
        raw_data = f.read().split('\n')
        for line in raw_data:
            if line == '':
                continue
            node, comm = map(eval, line.split())
            node2comm[node] = comm
            if comm in comm_size:
                comm_size[comm] += 1
            else:
                comm_size[comm] = 1
    with open(graph_path, 'r') as f:
        raw_data = f.read().split('\n')
        for line in raw_data:
            if line == '':
                continue
            src, des = map(eval, line.split())
            if node2comm[src] == node2comm[des]:
                if node2comm[src] in comm_intra:
                    comm_intra[node2comm[src]] += 1
                else:
                    comm_intra[node2comm[src]] = 1
            else:
                if node2comm[src] in comm_inter:
                    comm_inter[node2comm[src]] += 1
                else:
                    comm_inter[node2comm[src]] = 1
                if node2comm[des] in comm_inter:
                    comm_inter[node2comm[des]] += 1
                else:
                    comm_inter[node2comm[des]] = 1
    dataset = list()
    for comm in comm_size:
        dataset.append({'comm': comm, 'size': comm_size[comm], 'intra_avg': 1.0 * comm_intra[comm] / comm_size[comm], 'inter_avg': 1.0 * comm_inter[comm] / comm_size[comm]})
    dataset = pd.DataFrame(dataset)
    dataset = dataset[['comm', 'size', 'intra_avg', 'inter_avg']]
    dataset.sort('size', ascending=0, inplace=True)
    dataset.to_csv(output_path, index=False, encoding='utf-8')


def get_robustness(file_path, LSCC_output_path, LWCC_output_path):
    frac_list = [0.0001, 0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    Graph, H = load_graph(file_path)
    InDegV = snap.TIntPrV()
    snap.GetNodeInDegV(Graph, InDegV)
    OutDegV = snap.TIntPrV()
    snap.GetNodeOutDegV(Graph, OutDegV)
    degree = dict()
    for item in InDegV:
        ID = item.GetVal1()
        InDeg = item.GetVal2()
        degree[ID] = InDeg
    for item in OutDegV:
        ID = item.GetVal1()
        OutDeg = item.GetVal2()
        degree[ID] += OutDeg
    sorted_degree = sorted(degree.items(), key=itemgetter(1), reverse=True)
    tot = len(sorted_degree)
    pos = [int(tot * frac) for frac in frac_list]
    print pos
    cur = 0
    LSCC_robust = list()
    LWCC_robust = list()
    for i in range(tot):
        Graph.DelNode(sorted_degree[i][0])
        if i == pos[cur] - 1:
            LSCC_frac = snap.GetMxSccSz(Graph)
            LWCC_frac = snap.GetMxWccSz(Graph)
            singleton_frac = 1.0 - 1.0 * snap.CntNonZNodes(Graph) / Graph.GetNodes()
            LSCC_robust.append({'removed': frac_list[cur], 'singleton': singleton_frac, 'middle': 1.0 - singleton_frac - LSCC_frac, 'LSCC': LSCC_frac})
            LWCC_robust.append({'removed': frac_list[cur], 'singleton': singleton_frac, 'middle': 1.0 - singleton_frac - LWCC_frac, 'LWCC': LWCC_frac})
            cur += 1
        if cur >= len(pos):
            break
    LSCC_robust = pd.DataFrame(LSCC_robust)
    LSCC_robust = LSCC_robust[['removed', 'singleton', 'middle', 'LSCC']]
    LSCC_robust.to_csv(LSCC_output_path, index=False, encoding='utf-8')
    LWCC_robust = pd.DataFrame(LWCC_robust)
    LWCC_robust = LWCC_robust[['removed', 'singleton', 'middle', 'LWCC']]
    LWCC_robust.to_csv(LWCC_output_path, index=False, encoding='utf-8')
