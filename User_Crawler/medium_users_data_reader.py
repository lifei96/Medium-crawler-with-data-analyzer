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
        try:
            file_in = open('./data/Users/%s.json' % username, 'r')
            raw_data = json.loads(str(file_in.read()))
            file_in.close()
            user = dict()
            user['username'] = username
            user['reg_date'] = datetime.date.fromtimestamp(raw_data['profile']['user']['createdAt']/1000.0).isoformat()
            if not raw_data['profile']['user']['lastPostCreatedAt']:
                raw_data['profile']['user']['lastPostCreatedAt'] = raw_data['profile']['user']['createdAt']
            user['last_post_date'] = datetime.date.fromtimestamp(raw_data['profile']['user']['lastPostCreatedAt']/1000.0).isoformat()
            user['posts_count'] = raw_data['profile']['numberOfPostsPublished']
            user['following_count'] = raw_data['profile']['user']['socialStats']['usersFollowedCount']
            user['followers_count'] = raw_data['profile']['user']['socialStats']['usersFollowedByCount']
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

    users_data.to_csv('./result/users_raw_data.csv', sep='\t', encoding='utf-8')
