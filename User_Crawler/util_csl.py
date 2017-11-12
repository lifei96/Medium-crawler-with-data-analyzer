# -*- coding: utf-8 -*-

import pandas as pd
import os
import json
from datetime import *
import jellyfish
from sklearn.feature_extraction.text import TfidfVectorizer
from guess_language import guess_language
from wordcloud import WordCloud
import matplotlib.pyplot as plt


USER_ATTR_LIST = ['./data/cross-site-linking/user_type.csv',
                  './data/graph/CC.csv',
                  './data/graph/degree.csv',
                  './data/graph/pagerank.csv',
                  './data/cross-site-linking/user_attr_other.csv',
                  './data/cross-site-linking/username.csv'
                  ]

TWITTER_ATTR_LIST = ['./data/cross-site-linking/user_attr_str.csv',
                     './data/cross-site-linking/twitter_attr.csv']


def get_user_type_dict():
    user_type_path = './data/cross-site-linking/user_type.csv'
    return load_user_attr_to_dict(user_type_path)


def timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y%m%d')


def df_output(df, output_path):
    df.to_csv(output_path, index=False, encoding='utf-8')


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
    return pd.read_csv(file_path, encoding='utf-8', engine='python')


def load_all_attr_to_df(file_list=USER_ATTR_LIST):
    try:
        df_list = [load_user_attr_to_df(file_path) for file_path in file_list]
    except Exception as e:
        print type(e)
        print e.args
        print e
        return e
    res = df_list[0]
    for i in range(1, len(df_list)):
        res = pd.merge(res, df_list[i], on='username')
    return res


def split_df(df, output_path_prefix, by='user_type'):
    by_value_list = sorted(df[by].drop_duplicates().values.tolist())
    for by_value in by_value_list:
        splited = df[df[by] == by_value]
        df_output(splited, output_path_prefix + str(by_value) + '.csv')


def extract_user_attr_num():
    user_attr_list = []
    user_file_path = './data/Users/'
    dir_path_list = os.listdir(user_file_path)
    cnt = 0
    tot = len(dir_path_list)
    for filename in dir_path_list:
        if filename.endswith('.json'):
            file_path = os.path.join(user_file_path, filename)
            with open(file_path, 'r') as f:
                try:
                    user_data = json.load(f)
                    user_data_dict = dict()
                    user_data_dict['username'] = user_data['profile']['user']['username']
                    user_data_dict['posts'] = user_data['profile']['numberOfPostsPublished']
                    user_data_dict['recommends'] = len(user_data['recommends'])
                    user_data_dict['responses'] = len(user_data['responses'])
                    user_data_dict['highlights'] = len(user_data['highlights'])
                    user_data_dict['created_at'] = user_data['profile']['user']['createdAt'] / 1000.0
                    if user_data['profile']['user']['bio'] == '':
                        user_data_dict['bio_bin'] = 0
                    else:
                        user_data_dict['bio_bin'] = 1
                    user_attr_list.append(user_data_dict)
                except:
                    print file_path
        cnt += 1
        print '%d/%d' % (cnt , tot)
    user_attr_df = pd.DataFrame(user_attr_list)
    df_output(user_attr_df, './data/cross-site-linking/user_attr_other.csv')


def get_csl_ratio_by_bin_attr(file_path='./data/cross-site-linking/user_attr.csv', attr='bio_bin'):
    user_attr_df = load_user_attr_to_df(file_path)
    df_0 = user_attr_df[user_attr_df[attr] == 0]
    df_1 = user_attr_df[user_attr_df[attr] == 1]
    row_0 = df_0.shape[0]
    row_1 = df_1.shape[0]
    print attr + ': ' + '0'
    print row_0
    for i in range(4):
        print str(i) + ': ' + str(df_0[df_0['user_type'] == i].shape[0] / float(row_0))
    print '\n'
    print attr + ': ' + '1'
    print row_1
    for i in range(4):
        print str(i) + ': ' + str(df_1[df_1['user_type'] == i].shape[0] / float(row_1))


def get_date_type(file_path='./data/cross-site-linking/user_attr.csv'):
    user_attr_df = load_user_attr_to_df(file_path)
    type_time_df = user_attr_df[['user_type', 'created_at']]
    type_time_df = type_time_df.sort_values(by='created_at')
    date_type_list = []
    for idx, row in type_time_df.iterrows():
        date_type_dict = {}
        date_type_dict['created_date'] = timestamp_to_date(row['created_at'])
        date_type_dict['user_type'] = row['user_type']
        date_type_list.append(date_type_dict)
    res = pd.DataFrame(date_type_list)
    df_output(res, './data/cross-site-linking/date_type.csv')


def get_date_username(file_path='./data/cross-site-linking/user_attr.csv'):
    user_attr_df = load_user_attr_to_df(file_path)
    type_time_df = user_attr_df[['username', 'created_at']]
    type_time_df = type_time_df.sort_values(by='created_at')
    date_type_list = []
    for idx, row in type_time_df.iterrows():
        date_type_dict = {}
        date_type_dict['created_date'] = timestamp_to_date(row['created_at'])
        date_type_dict['username'] = row['username']
        date_type_list.append(date_type_dict)
    res = pd.DataFrame(date_type_list)
    df_output(res, './data/cross-site-linking/date_username.csv')


def get_date_csl_ratio(file_path='./data/cross-site-linking/date_type.csv'):
    date_type_df = load_user_attr_to_df(file_path)
    date_csl_list = []
    csl_num = [0, 0, 0, 0, 0]
    cur_date = ''
    for idx, row in date_type_df.iterrows():
        if cur_date == '':
            cur_date = row['created_date']
        if cur_date != row['created_date']:
            date_csl_dict = {}
            date_csl_dict['date'] = cur_date
            tot = sum(csl_num)
            for i in range(4):
                date_csl_dict[str(i)] = float(csl_num[i]) / tot
            date_csl_dict['4'] = csl_num[4]
            date_csl_list.append(date_csl_dict)
            cur_date = row['created_date']
        csl_num[int(row['user_type'])] += 1
        csl_num[4] += 1
    date_csl_dict = {}
    date_csl_dict['date'] = cur_date
    tot = sum(csl_num)
    for i in range(4):
        date_csl_dict[str(i)] = float(csl_num[i]) / tot
    date_csl_dict['4'] = csl_num[4]
    date_csl_list.append(date_csl_dict)
    date_csl_df = pd.DataFrame(date_csl_list)
    df_output(date_csl_df, './data/cross-site-linking/date_csl_ratio.csv')


def get_twitter_attr(file_path='./data/cross-site-linking/user_attr.csv'):
    user_attr_df = load_user_attr_to_df(file_path)
    username_list = user_attr_df['username'].tolist()
    user_data_list = []
    tot = len(username_list)
    cnt = 0
    for username in username_list:
        twitter_file_path = './data/Twitter/%s_t.json' % username
        if os.path.exists(twitter_file_path):
            with open(twitter_file_path, 'r') as f:
                try:
                    user_data = json.load(f)['profile_user']
                    user_data_dict = dict()
                    user_data_dict['username'] = username
                    user_data_dict['t_des'] = user_data['description']
                    if 'location' in user_data:
                        user_data_dict['t_loc'] = user_data['location']
                    else:
                        user_data_dict['t_loc'] = ''
                    user_data_dict['t_name'] = user_data['name']
                    if 'lang' in user_data:
                        user_data_dict['t_lang'] = user_data['lang']
                    else:
                        user_data_dict['t_lang'] = ''
                    user_data_dict['t_username'] = user_data['screen_name']
                    if 'created_at' in user_data:
                        user_data_dict['t_created_at'] = datetime.strptime(user_data['created_at'], '%a %b %d %X +0000 %Y').strftime('%Y%m%d')
                    else:
                        user_data_dict['t_created_at'] = ''
                    if 'time_zone' in user_data:
                        user_data_dict['t_time_zone'] = user_data['time_zone']
                    else:
                        user_data_dict['t_time_zone'] = ''
                    user_data_list.append(user_data_dict)
                except Exception as e:
                    print twitter_file_path
                    print type(e)
                    print e.args
                    print e
        cnt += 1
        print '%d/%d' % (cnt, tot)
    twitter_attr_df = pd.DataFrame(user_data_list)
    df_output(twitter_attr_df, './data/cross-site-linking/twitter_attr.csv')


def merge_twitter_attr():
    df = load_all_attr_to_df(TWITTER_ATTR_LIST)
    df_output(df, './data/cross-site-linking/user_twitter_attr.csv')


def extract_user_attr_str():
    user_attr_list = []
    user_file_path = './data/Users/'
    dir_path_list = os.listdir(user_file_path)
    cnt = 0
    tot = len(dir_path_list)
    for filename in dir_path_list:
        if filename.endswith('.json'):
            file_path = os.path.join(user_file_path, filename)
            with open(file_path, 'r') as f:
                try:
                    user_data = json.load(f)
                    user_data_dict = dict()
                    user_data_dict['username'] = user_data['profile']['user']['username']
                    user_data_dict['bio'] = user_data['profile']['user']['bio']
                    user_data_dict['name'] = user_data['profile']['user']['name']
                    user_attr_list.append(user_data_dict)
                except:
                    print file_path
        cnt += 1
        print '%d/%d' % (cnt, tot)
    user_attr_df = pd.DataFrame(user_attr_list)
    df_output(user_attr_df, './data/cross-site-linking/user_attr_str.csv')


def word_similarity(s1, s2):
    return jellyfish.jaro_winkler(unicode(s1.lower()), unicode(s2.lower()))


def sentence_similarity(s1, s2):
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform([s1, s2])
    return (tfidf * tfidf.T).A[0][1]


def get_similarity(file_path='./data/cross-site-linking/user_twitter_attr.csv'):
    user_twitter_df = load_user_attr_to_df(file_path)
    user_twitter_df.fillna('', inplace=True)
    username_simi_list = []
    name_simi_list = []
    bio_simi_list = []
    tot = user_twitter_df.shape[0]
    cnt = 0
    for idx, row in user_twitter_df.iterrows():
        try:
            username = row['username']
            t_username = row['t_username']
            name = row['name']
            t_name = row['t_name']
            bio = row['bio']
            t_bio = row['t_des']
            if username is not '' or t_username is not '':
                score = word_similarity(username, t_username)
                username_simi_list.append({'username': username, 'similarity_username': score})
            if name is not '' or t_name is not '':
                score = word_similarity(name, t_name)
                name_simi_list.append({'username': username, 'similarity_name': score})
            if bio is not '' or t_bio is not '':
                score = sentence_similarity(bio, t_bio)
                bio_simi_list.append({'username': username, 'similarity_bio': score})
        except Exception as e:
            print type(e)
            print e.args
            print e
        cnt += 1
        print '%d/%d' % (cnt, tot)
    username_simi_df = pd.DataFrame(username_simi_list)
    name_simi_df = pd.DataFrame(name_simi_list)
    bio_simi_df = pd.DataFrame(bio_simi_list)
    df_output(username_simi_df, './data/cross-site-linking/username_simi.csv')
    df_output(name_simi_df, './data/cross-site-linking/name_simi.csv')
    df_output(bio_simi_df, './data/cross-site-linking/bio_simi.csv')


def get_txt(df, field, output_path):
    df.fillna('', inplace=True)
    output_str = ''
    tot = df.shape[0]
    cnt = 0
    for idx, row in df.iterrows():
        try:
            if row[field] is not '' and guess_language(row[field]) == 'en':
                output_str += (row[field].encode('utf-8') + '\n')
        except Exception as e:
            print type(e)
            print e.args
            print e
        cnt += 1
        print '%d/%d' % (cnt, tot)
    with open(output_path, 'w') as f:
        f.write(output_str.replace('&amp', ''))


def split_bio_to_txt(file_path='./data/cross-site-linking/user_attr_str.csv'):
    user_type_path = './data/cross-site-linking/user_type.csv'
    user_str_df = load_all_attr_to_df([file_path, user_type_path])
    user_str_df.fillna('', inplace=True)
    output_str = ['', '', '', '']
    tot = user_str_df.shape[0]
    cnt = 0
    for idx, row in user_str_df.iterrows():
        try:
            bio = row['bio'].encode('utf-8')
            user_type = row['user_type']
            if bio != '':
                output_str[user_type] += (bio.encode('utf-8') + '\n')
        except Exception as e:
            print type(e)
            print e.args
            print e
        cnt += 1
        print '%d/%d' % (cnt, tot)
    for i in range(4):
        with open('./data/cross-site-linking/bio_%d.txt' % i, 'w') as f:
            f.write(output_str[i])
    with open('./data/cross-site-linking/bio_all.txt', 'w') as f:
        f.write('\n'.join(output_str))


def get_wordcloud(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    wordcloud = WordCloud(max_font_size=200, min_font_size=25, prefer_horizontal=1, background_color='white', margin=0,
                          relative_scaling=0.5, colormap='copper', collocations=False, width=1600, height=800).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def split_similarity():
    username_simi_path = './data/cross-site-linking/username_simi.csv'
    name_simi_path = './data/cross-site-linking/name_simi.csv'
    bio_simi_path = './data/cross-site-linking/bio_simi.csv'
    user_type_path = './data/cross-site-linking/user_type.csv'
    username_df = load_all_attr_to_df([username_simi_path, user_type_path])
    name_df = load_all_attr_to_df([name_simi_path, user_type_path])
    bio_df = load_all_attr_to_df([bio_simi_path, user_type_path])
    split_df(username_df, './data/cross-site-linking/username_simi_')
    split_df(name_df, './data/cross-site-linking/name_simi_')
    split_df(bio_df, './data/cross-site-linking/bio_simi_')


def get_tags(username):
    with open('./data/Users/%s.json' % username, 'r') as f:
        user_data = json.load(f)
    tags = []
    try:
        for tag in user_data['profile']['interestTags']:
            tags.append(tag['name'].encode('utf-8'))
    except Exception as e:
        print type(e)
        print e.args
        print e
    return tags


def split_tags_to_txt():
    user_type_path = './data/cross-site-linking/user_type.csv'
    user_type_df = load_user_attr_to_df(user_type_path)
    output_str = ['', '', '', '']
    tot = user_type_df.shape[0]
    cnt = 0
    for idx, row in user_type_df.iterrows():
        try:
            username = row['username']
            tags = get_tags(username)
            user_type = row['user_type']
            if len(tags) > 0:
                output_str[user_type] += ('\n'.join(tags) + '\n').encode('utf-8')
        except Exception as e:
            print type(e)
            print e.args
            print e
        cnt += 1
        print '%d/%d' % (cnt, tot)
    for i in range(4):
        with open('./data/cross-site-linking/tag_%d.txt' % i, 'w') as f:
            f.write(output_str[i])
    with open('./data/cross-site-linking/tag_all.txt', 'w') as f:
        f.write('\n'.join(output_str))


def get_degree_in_graph_csl():
    user_type_dict = get_user_type_dict()
    degree_df = load_user_attr_to_df('./data/graph/degree_in_graph.csv')
    user_type = []
    for username in degree_df['username']:
        if username in user_type_dict:
            user_type.append(user_type_dict[username]['user_type'])
        else:
            user_type.append(-1)
    degree_df['user_type'] = user_type
    split_df(degree_df, './data/cross-site-linking/user_degree_in_graph_')


def get_CC_csl():
    user_type_dict = get_user_type_dict()
    cc_df = load_user_attr_to_df('./data/graph/cc_20160801.csv')
    user_type = []
    for username in cc_df['username']:
        if username in user_type_dict:
            user_type.append(user_type_dict[username]['user_type'])
        else:
            user_type.append(-1)
    cc_df['user_type'] = user_type
    split_df(cc_df, './data/cross-site-linking/user_cc_')
