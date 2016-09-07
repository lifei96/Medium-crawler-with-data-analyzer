# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os


def posts_data_parser():
    if not os.path.exists('./result'):
        os.mkdir('./result')

    posts_data = pd.read_csv('./result/posts_raw_data.csv', sep='\t', encoding='utf-8')

    posts_data['published_date'] = pd.to_datetime(posts_data['published_date'], errors='coerce')

    mask = (posts_data['published_date'] >= datetime.datetime(2013, 1, 1)) & (posts_data['published_date'] <= datetime.datetime(2016, 6, 30))
    posts_data = posts_data.loc[mask]

    plt.figure(figsize=(20, 10))
    plt.axis([datetime.datetime(2013, 1, 1), datetime.datetime(2016, 6, 30), 0, 7000])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    posts_data.groupby(['published_date'])[['post_id']].count().rename(columns={'post_id': 'post_count'}).plot(ax=ax)
    plt.savefig('./result/new_posts_per_day.png')
    plt.close()

    recommends_count_list = np.sort(posts_data['recommends'].tolist())
    plt.figure(figsize=(20, 15))
    plt.axis([0, 200, 0, 1])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.plot(recommends_count_list, np.linspace(0, 1, recommends_count_list.size))
    plt.savefig('./result/CDF_post_recommends_count.png')
    plt.close()

    responses_count_list = np.sort(posts_data['responses'].tolist())
    plt.figure(figsize=(20, 15))
    plt.axis([0, 20, 0, 1])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.plot(responses_count_list, np.linspace(0, 1, responses_count_list.size))
    plt.savefig('./result/CDF_post_responses_count.png')
    plt.close()

if __name__ == '__main__':
    posts_data_parser()
