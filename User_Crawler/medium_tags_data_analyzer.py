# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os


def tags_data_parser():
    if not os.path.exists('./result'):
        os.mkdir('./result')

    tags_data = pd.read_csv('./result/tags_raw_data.csv', sep='\t', encoding='utf-8')

    tags_data['published_date'] = pd.to_datetime(tags_data['published_date'], errors='coerce')

    mask = (tags_data['published_date'] >= datetime.datetime(2013, 1, 1)) & (tags_data['published_date'] <= datetime.datetime(2016, 6, 30))
    tags_data = tags_data.loc[mask]
    tags_data['weekday'] = [date.isoweekday() for date in tags_data['published_date']]

    tags_data_grouped = tags_data.groupby('tag')
    tags_data_result = tags_data_grouped.agg({'post_id': 'count', 'recommends': 'mean', 'responses': 'mean'})
    tags_data_result = tags_data_result.rename(columns={'post_id': 'count', 'recommends': 'recommends_mean', 'responses': 'responses_mean'})
    tags_data_result = tags_data_result.sort_values(by='count', ascending=0)
    tags_data_result.to_csv('./result/tags_rank.csv', sep='\t', encoding='utf-8')

    fig, axes = plt.subplots(nrows=2, ncols=2)
    tags_data_result[0:49].plot(y='count', kind='barh', fontsize=10, ax=axes[0, 0], figsize=(15, 15))
    axes[0, 0].invert_yaxis()

    tags_data_result = tags_data_result.loc[tags_data_result['count'] >= 100]

    tags_data_result = tags_data_result.sort_values(by='recommends_mean', ascending=0)
    tags_data_result[0:49].plot(y='recommends_mean', kind='barh', fontsize=10, ax=axes[1, 0], figsize=(15, 15))
    axes[1, 0].invert_yaxis()

    tags_data_result = tags_data_result.sort_values(by='responses_mean', ascending=0)
    tags_data_result[0:49].plot(y='responses_mean', kind='barh', fontsize=10, ax=axes[1, 1], figsize=(15, 15))
    axes[1, 1].invert_yaxis()

    tags_top_list = list(tags_data_result.index)
    mask = (tags_data['recommends'] >= 20) & (tags_data['tag'].isin(tags_top_list))
    tags_data_tmp = tags_data.loc[mask]
    tags_data_tmp['responses/recommends'] = tags_data_tmp['responses']/tags_data_tmp['recommends']
    tags_data_grouped = tags_data_tmp.groupby('tag')
    tags_data_result = tags_data_grouped.agg({'post_id': 'count', 'recommends': 'mean', 'responses': 'mean', 'responses/recommends': 'mean'})
    tags_data_result = tags_data_result.rename(columns={'post_id': 'count', 'recommends': 'recommends_mean', 'responses': 'responses_mean', 'responses/recommends': 'responses/recommends_mean'})
    tags_data_result = tags_data_result.sort_values(by='responses/recommends_mean', ascending=0)
    tags_data_result[0:49].plot(y='responses/recommends_mean', kind='barh', fontsize=10, ax=axes[0, 1], figsize=(15, 15))
    axes[0, 1].invert_yaxis()

    [ax.legend(loc=0, prop={'size': 14}) for ax in plt.gcf().axes]
    plt.tight_layout()
    fig.savefig('./result/tags_rank.png')
    plt.close()


if __name__ == '__main__':
    tags_data_parser()
