# -*- coding: utf-8 -*-

import pandas as pd
import json
import datetime
import os


def read_posts():
    posts = list()
    file_in = open('./post_list.txt', 'r')
    post_list = str(file_in.read()).split(' ')
    file_in.close()
    num = 0
    for post_id in post_list:
        if not post_id:
            continue
        if not os.path.exists('./data/Posts/%s.json' % post_id):
            continue
        try:
            file_in = open('./data/Posts/%s.json' % post_id, 'r')
            raw_data = json.loads(str(file_in.read()))
            file_in.close()
            for tag in raw_data['tags']:
            	post = dict()
            	post['post_id'] = post_id
            	post['published_date'] = raw_data['published_date']
            	post['recommends'] = raw_data['recommends']
            	post['responses'] = raw_data['responses']
                post['tag'] = tag['name']
                posts.append(post)
                print(post)
        except:
            continue
        num += 1
        print(post_id)
        print(num)
    return pd.read_json(json.dumps(posts))

if __name__ == '__main__':
    if not os.path.exists('./result'):
        os.mkdir('./result')

    posts_data = read_posts()

    posts_data.to_csv('./result/tags_raw_data.csv', sep='\t', encoding='utf-8')
