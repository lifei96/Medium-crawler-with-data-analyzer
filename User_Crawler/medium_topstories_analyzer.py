# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import datetime
import os


START_DATE = datetime.date(2014, 9, 10)
END_DATE = datetime.date(2016, 7, 16)


def read_stories_without_tags():
    stories = list()
    current_date = START_DATE
    while current_date <= END_DATE:
        file_in = open("./TopStories/%s.json" % current_date.isoformat(), 'r')
        raw_data = json.loads(str(file_in.read()))
        file_in.close()
        for raw_story in raw_data['stories']:
            story = dict()
            story['top_date'] = current_date.isoformat()
            story['story_id'] = raw_story['story_id']
            story['author'] = raw_story['author']
            story['published_date'] = raw_story['published_date']
            story['recommends'] = raw_story['recommends']
            story['responses'] = raw_story['responses']
            story['tags_count'] = len(raw_story['tags'])
            stories.append(story)
        print(current_date.isoformat())
        current_date = current_date + datetime.timedelta(days=1)
    return pd.read_json(json.dumps(stories))


def read_stories_by_tags():
    tags = list()
    current_date = START_DATE
    while current_date <= END_DATE:
        file_in = open("./TopStories/%s.json" % current_date.isoformat(), 'r')
        raw_data = json.loads(str(file_in.read()))
        file_in.close()
        for raw_story in raw_data['stories']:
            for raw_tag in raw_story['tags']:
                tag = dict()
                tag['top_date'] = current_date.isoformat()
                tag['story_id'] = raw_story['story_id']
                tag['author'] = raw_story['author']
                tag['published_date'] = raw_story['published_date']
                tag['recommends'] = raw_story['recommends']
                tag['responses'] = raw_story['responses']
                tag['name'] = raw_tag['name']
                tag['post_count'] = raw_tag['postCount']
                tag['follower_count'] = raw_tag['metadata']['followerCount']
                tags.append(tag)
        print(current_date.isoformat())
        current_date = current_date + datetime.timedelta(days=1)
    return pd.read_json(json.dumps(tags))


if __name__ == '__main__':
    if not os.path.exists('./top_stories_result'):
        os.mkdir('./top_stories_result')

    stories_data = read_stories_without_tags()
    tags_data = read_stories_by_tags()

    stories_data.to_csv('./top_stories_result/stories_raw_data.csv', sep='\t', encoding='utf-8')

    tags_data.to_csv('./top_stories_result/tags_raw_data.csv', sep='\t', encoding='utf-8')

    plt.figure()
    stories_data.groupby(['top_date'])[['recommends']].mean().plot()
    plt.savefig('./top_stories_result/recommends-top_date.png')
    plt.close()

    plt.figure()
    stories_data.groupby(['top_date'])[['responses']].mean().plot()
    plt.savefig('./top_stories_result/responses-top_date.png')
    plt.close()

    plt.figure()
    stories_data.groupby(['top_date'])[['recommends', 'responses']].mean().plot()
    plt.savefig('./top_stories_result/recommends_responses-top_date.png')
    plt.close()

    plt.figure()
    stories_data.groupby(['top_date'])[['tags_count']].mean().plot()
    plt.savefig('./top_stories_result/tags_count-top_date.png')
    plt.close()

    stories_data.groupby(['author'])[['story_id']].count().rename(columns={'story_id': 'count'}).sort_values(by=['count'], ascending=False).to_csv('./top_stories_result/author_count.csv', sep='\t', encoding='utf-8')

    stories_data.groupby(['story_id'])[['author']].count().rename(columns={'author': 'count'}).sort_values(by=['count'], ascending=False).to_csv('./top_stories_result/story_count.csv', sep='\t', encoding='utf-8')

    tags_data.groupby(['name'])[['story_id']].count().rename(columns={'story_id': 'count'}).sort_values(by=['count'], ascending=False).to_csv('./top_stories_result/tags_count.csv', sep='\t', encoding='utf-8')

    responses_list = np.sort(stories_data['responses'].tolist())
    plt.figure()
    plt.plot(responses_list, np.linspace(0, 1, responses_list.size))
    plt.savefig('./top_stories_result/CDF_responses.png')
    plt.close()

    recommends_list = np.sort(stories_data['recommends'].tolist())
    plt.figure()
    plt.plot(recommends_list, np.linspace(0, 1, recommends_list.size))
    plt.savefig('./top_stories_result/CDF_recommends.png')
    plt.close()

    tags_count_list = np.sort(stories_data['tags_count'].tolist())
    plt.figure()
    plt.plot(tags_count_list, np.linspace(0, 1, tags_count_list.size))
    plt.savefig('./top_stories_result/CDF_tags_count.png')
    plt.close()

    tags_post_count_count = tags_data[['name', 'post_count']].drop_duplicates().join(tags_data.groupby(['name'])[['story_id']].count().rename(columns={'story_id': 'count'}), on='name')
    plt.figure()
    tags_post_count_count[['post_count', 'count']].plot(x='post_count', y='count', kind='scatter')
    plt.savefig('./top_stories_result/tags_count-post_count.png')
    plt.close()

    tags_follower_count_count = tags_data[['name', 'follower_count']].drop_duplicates().join(tags_data.groupby(['name'])[['story_id']].count().rename(columns={'story_id': 'count'}), on='name')
    plt.figure()
    tags_follower_count_count[['follower_count', 'count']].plot(x='follower_count', y='count', kind='scatter')
    plt.savefig('./top_stories_result/tags_count-follower_count.png')
    plt.close()
