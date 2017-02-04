# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
import os


def users_data_parser():
    if not os.path.exists('./result'):
        os.mkdir('./result')

    file_in = open('./suspended_username_list.txt', 'r')
    suspended_username_list = str(file_in.read()).split(' ')
    file_in.close()

    users_data = pd.read_csv('./result/users_raw_data.csv', sep='\t', encoding='utf-8')

    users_data['last_post_date'] = pd.to_datetime(users_data['last_post_date'], errors='coerce')
    users_data['reg_date'] = pd.to_datetime(users_data['reg_date'], errors='coerce')

    mask = (users_data['reg_date'] >= datetime.datetime(2013, 1, 1)) & (users_data['reg_date'] <= datetime.datetime(2016, 6, 30))
    users_data = users_data.loc[mask]
    mask = users_data['username'].isin(suspended_username_list)
    suspended_users_data = users_data.loc[mask]

    twitter_data = pd.read_csv('./result/twitter.csv', sep='\t', encoding='utf-8')

    f_f_list = np.sort(((users_data['following_count'] + 0.1) / (users_data['followers_count'] + 0.1)).tolist())
    f_f_list2 = np.sort(((twitter_data['following_count'] + 0.1) / (twitter_data['followers_count'] + 0.1)).tolist())
    t_f_f_list = np.sort(((twitter_data['t_following_count'] + 0.1) / (twitter_data['t_followers_count'] + 0.1)).tolist())
    s_f_f_list = np.sort(((suspended_users_data['following_count'] + 0.1) / (suspended_users_data['followers_count'] + 0.1)).tolist())

    plt.figure(figsize=(15, 10))
    plt.axis([0.01, 1000, 0, 1])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.xlabel('(following+0.1)/(followers+0.1)')
    plt.ylabel('CDF')
    plt.yticks(np.linspace(0, 1, 21))
    plt.grid()
    plt.title('Balance')
    line1, = plt.semilogx(f_f_list, np.linspace(0, 1, f_f_list.size), '-g')
    line2, = plt.semilogx(f_f_list2, np.linspace(0, 1, f_f_list2.size), '-r')
    line3, = plt.semilogx(t_f_f_list, np.linspace(0, 1, t_f_f_list.size), '-b')
    line4, = plt.semilogx(s_f_f_list, np.linspace(0, 1, s_f_f_list.size), '--g')
    plt.legend((line1, line2, line3, line4), ("all Medium users", "Medium users connected to Twitter", "Twitter users", "Medium users whose Twitter are suspended"), loc=2)
    plt.savefig('./result/CDF_balance.png')
    plt.close()

    reciprocity_data = pd.read_csv('./result/reciprocity.csv', sep='\t', encoding='utf-8')

    reciprocity_list = np.sort(((reciprocity_data['reciprocity_count'] + 0.0000000001) / (reciprocity_data['following_count'] + 0.0000000001)).tolist())
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.xlabel('friends/following')
    plt.ylabel('CDF')
    plt.yticks(np.linspace(0, 1, 21))
    plt.xticks(np.linspace(0, 1, 21))
    plt.grid()
    plt.title('Reciprocity')
    plt.plot(reciprocity_list, np.linspace(0, 1, reciprocity_list.size), label='Reciprocity')
    plt.savefig('./result/CDF_reciprocity.png')
    plt.close()

    f_f_list = np.sort((users_data['following_count']).tolist())
    s_f_f_list = np.sort((suspended_users_data['following_count']).tolist())

    plt.figure(figsize=(15, 10))
    plt.axis([1, 1000, 0, 1])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.xlabel('following')
    plt.ylabel('CDF')
    plt.grid()
    plt.title('CDF_following')
    line1, = plt.semilogx(f_f_list, np.linspace(0, 1, f_f_list.size), '-g')
    line2, = plt.semilogx(s_f_f_list, np.linspace(0, 1, s_f_f_list.size), '-b')
    plt.legend((line1, line2), ("all Medium users", "Medium users whose Twitter are suspended"), loc=4)
    plt.savefig('./result/CDF_following.png')
    plt.close()

    f_f_list = np.sort((users_data['followers_count']).tolist())
    s_f_f_list = np.sort((suspended_users_data['followers_count']).tolist())

    plt.figure(figsize=(15, 10))
    plt.axis([1, 2000, 0, 1])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.xlabel('followers')
    plt.ylabel('CDF')
    plt.grid()
    plt.title('CDF_followers')
    line1, = plt.semilogx(f_f_list, np.linspace(0, 1, f_f_list.size), '-g')
    line2, = plt.semilogx(s_f_f_list, np.linspace(0, 1, s_f_f_list.size), '-b')
    plt.legend((line1, line2), ("all Medium users", "Medium users whose Twitter are suspended"), loc=4)
    plt.savefig('./result/CDF_followers.png')
    plt.close()

    f_f_list = np.sort((users_data['posts_count']).tolist())
    s_f_f_list = np.sort((suspended_users_data['posts_count']).tolist())

    plt.figure(figsize=(15, 10))
    plt.axis([1, 50, 0, 1])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.xlabel('posts')
    plt.ylabel('CDF')
    plt.grid()
    plt.title('CDF_posts')
    line1, = plt.semilogx(f_f_list, np.linspace(0, 1, f_f_list.size), '-g')
    line2, = plt.semilogx(s_f_f_list, np.linspace(0, 1, s_f_f_list.size), '-b')
    plt.legend((line1, line2), ("all Medium users", "Medium users whose Twitter are suspended"), loc=4)
    plt.savefig('./result/CDF_posts.png')
    plt.close()

    mean_median_list = [[users_data['following_count'].mean(), suspended_users_data['following_count'].mean()],
                        [users_data['following_count'].median(), suspended_users_data['following_count'].median()],
                        [users_data['followers_count'].mean(), suspended_users_data['followers_count'].mean()],
                        [users_data['followers_count'].median(), suspended_users_data['followers_count'].median()],
                        [users_data['posts_count'].mean(), suspended_users_data['posts_count'].mean()],
                        [users_data['posts_count'].median(), suspended_users_data['posts_count'].median()]]
    mean_median = pd.DataFrame(mean_median_list, columns=['All users', 'Suspended users'])
    ax = mean_median.plot.bar(figsize=(15, 10), fontsize=16)
    ax.set_xticks(mean_median.index)
    ax.set_xticklabels(['following_mean', 'following_median', 'followers_mean', 'followers_median', 'posts_mean', 'posts_median'], rotation=0)
    plt.savefig('./result/mean_median.png')
    plt.close()


if __name__ == '__main__':
    users_data_parser()
