# -*- coding: utf-8 -*-

import pandas as pd
import json
import datetime
import os


def read_users():
    users = list()
    file_in = open('./username_list.txt', 'r')
    username_list = str(file_in.read()).split(' ')
    file_in.close()
    num = 0
    for username in username_list:
        if not username:
            continue
        if not os.path.exists('./data/Users/%s.json' % username):
            continue
        if not os.path.exists('./data/Twitter/%s_t.json' % username):
            continue
        try:
            file_in = open('./data/Users/%s.json' % username, 'r')
            raw_data = json.loads(str(file_in.read()))
            file_in.close()
            user = dict()
            user['followers_count'] = raw_data['profile']['user']['socialStats']['usersFollowedByCount']
            user['following_count'] = raw_data['profile']['user']['socialStats']['usersFollowedCount']
            file_in = open('./data/Twitter/%s_t.json' % username, 'r')
            raw_data = json.loads(str(file_in.read()))
            file_in.close()
            user['t_following_count'] = raw_data['profile_user']['friends_count']
            user['t_followers_count'] = raw_data['profile_user']['followers_count']
            users.append(user)
        except:
            continue
        num += 1
        print(username)
        print(num)
    return pd.read_json(json.dumps(users))

if __name__ == '__main__':
    if not os.path.exists('./result'):
        os.mkdir('./result')

    users_data = read_users()

    users_data.to_csv('./result/twitter.csv', sep='\t', encoding='utf-8')
