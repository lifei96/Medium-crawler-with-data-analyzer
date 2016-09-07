# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os


def users_data_parser():
    if not os.path.exists('./result'):
        os.mkdir('./result')

    users_data = pd.read_csv('./result/users_raw_data.csv', sep='\t', encoding='utf-8')

    users_data['last_post_date'] = pd.to_datetime(users_data['last_post_date'], errors='coerce')
    users_data['reg_date'] = pd.to_datetime(users_data['reg_date'], errors='coerce')

    mask = (users_data['reg_date'] >= datetime.datetime(2013, 1, 1)) & (users_data['reg_date'] <= datetime.datetime(2016, 6, 30))
    users_data = users_data.loc[mask]

    plt.figure(figsize=(20, 6))
    plt.axis([datetime.datetime(2013, 1, 1), datetime.datetime(2016, 6, 30), 0, 3000])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    users_data.groupby(['reg_date'])[['username']].count().rename(columns={'username': 'reg_count'}).plot(ax=ax)
    plt.savefig('./result/new_registration_per_day.png')
    plt.close()

    plt.figure(figsize=(50, 50))
    plt.scatter(users_data['last_post_date'].tolist(), users_data['reg_date'].tolist())
    plt.savefig('./result/reg_date-last_post_date.png')
    plt.close()

    posts_count_list = np.sort(users_data['posts_count'].tolist())
    plt.figure(figsize=(20, 15))
    plt.axis([0, 50, 0, 1])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.plot(posts_count_list, np.linspace(0, 1, posts_count_list.size))
    plt.savefig('./result/CDF_user_posts_count.png')
    plt.close()

    following_count_list = np.sort(users_data['following_count'].tolist())
    plt.figure(figsize=(20, 15))
    plt.axis([0, 1000, 0, 1])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.plot(following_count_list, np.linspace(0, 1, following_count_list.size))
    plt.savefig('./result/CDF_user_following_count.png')
    plt.close()

    followers_count_list = np.sort(users_data['followers_count'].tolist())
    plt.figure(figsize=(20, 15))
    plt.axis([0, 2000, 0, 1])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.plot(followers_count_list, np.linspace(0, 1, followers_count_list.size))
    plt.savefig('./result/CDF_user_followers_count.png')
    plt.close()

if __name__ == '__main__':
    users_data_parser()
