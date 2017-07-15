# -*- coding: utf-8 -*-

import pandas as pd

USER_ATTR_LIST = ['./data/cross-site-linking/user_type.csv',
                  './data/graph/CC.csv',
                  './data/graph/degree.csv',
                  './data/graph/pagerank.csv'
                  ]


def dict_merge(dict_1, dict_2):
    res = {}
    for key in dict_1:
        if key in dict_2:
            res[key] = {}
            res[key].update(dict_1[key])
            res[key].update(dict_2[key])
    return res


def load_user_attr_to_dict(file_path):
    user_attr_dict = {}
    user_attr_df = pd.read_csv(file_path)
    attr_list = list(user_attr_df)
    attr_list.remove('username')
    for idx, row in user_attr_df.iterrows():
        user_attr_dict[row['username']] = {}
        for attr in attr_list:
            user_attr_dict[row['username']][attr] = row[attr]
    return user_attr_dict


def load_all_attr_to_dict(file_list=USER_ATTR_LIST):
    res = {}
    for file_path in file_list:
        user_attr_dict = load_user_attr_to_dict(file_path)
        res = dict_merge(res, user_attr_dict)
    return res


def load_user_attr_to_df(file_path):
    return pd.read_csv(file_path)


def load_all_attr_to_df(file_list=USER_ATTR_LIST):
    df_list = [load_user_attr_to_df(file_path) for file_path in file_list]
    res = df_list[0]
    for i in range(1, len(df_list)):
        res = pd.merge(res, df_list[i], on='username')
    return res


def split_df(df, by='user_type'):
    by_value_list = sorted(df[by].drop_duplicates().values.tolist())
    for by_value in by_value_list:
        df[df[by] == by_value].to_csv('./data/cross-site-linking/user_attr_' + str(by_value) + '.csv', index=False, encoding='utf-8')
