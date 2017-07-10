# -*- coding: utf-8 -*-

import os
import json
import pandas as pd
from util_parser import *


def parser(user_pr_list):
    dataset = list()
    tot = len(user_pr_list)
    num = 0
    for username, pr in user_pr_list:
        print username, pr
        if os.path.exists('./data/Users/%s.json' % username):
            data = user_parser('./data/Users/%s.json' % username)
        else:
            continue
        if data['twitter'] == 1 and os.path.exists('./data/Twitter/%s_t.json' % username):
            data.update(twitter_parser('./data/Twitter/%s_t.json' % username))
        else:
            data.update(twitter_parser(''))
        data['PR'] = pr
        if pr >= 9.17538216764e-06:
            data['class_1'] = 1
        else:
            data['class_1'] = 0
        if pr >= 2.31964919865e-06:
            data['class_5'] = 1
        else:
            data['class_5'] = 0
        if pr >= 1.2888748487e-06:
            data['class_10'] = 1
        else:
            data['class_10'] = 0
        dataset.append(data)
        num += 1
        print "%d/%d" % (num, tot)
    dataset = pd.DataFrame(dataset)
    return dataset

if __name__ == '__main__':
    dataset = pd.read_csv('./data/graph/pagerank.csv')
    output = parser(dataset[['username', 'PR']].apply(tuple, axis=1).tolist())
    output.to_csv('./data/prediction/dataset.csv', index=False, encoding='utf-8')
