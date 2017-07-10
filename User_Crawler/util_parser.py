# -*- coding: utf-8 -*-

import json


def user_parser(file_path):
    with open(file_path, 'r') as f:
        raw_data = json.load(f)
    data = dict()
    data['username'] = raw_data['profile']['user']['username']
    if 'socialStats' in raw_data['profile']['user']:
        data['followers'] = raw_data['profile']['user']['socialStats']['usersFollowedByCount']
        data['following'] = raw_data['profile']['user']['socialStats']['usersFollowedCount']
    else:
        data['followers'] = len(raw_data['followers'])
        data['following'] = len(raw_data['following'])
    data['lastPostCreatedAt'] = raw_data['profile']['user']['lastPostCreatedAt']
    data['createdAt'] = raw_data['profile']['user']['createdAt']
    data['postsInMonthlyTop100'] = raw_data['profile']['postsInMonthlyTop100']
    if 'twitterScreenName' not in raw_data['profile']['user'] or raw_data['profile']['user']['twitterScreenName'] == '':
        data['twitter'] = 0
    else:
        data['twitter'] = 1
    if 'facebookAccountId' not in raw_data['profile']['user'] or raw_data['profile']['user']['facebookAccountId'] == '':
        data['facebook'] = 0
    else:
        data['facebook'] = 1
    if raw_data['profile']['user']['bio'] == '':
        data['bio'] = 0
    else:
        data['bio'] = 1
    data['posts'] = len(raw_data['latest'])
    data['highlights'] = len(raw_data['highlights'])
    data['responses'] = len(raw_data['responses'])
    data['recommends'] = len(raw_data['recommends'])
    data['authorTags'] = len(raw_data['profile']['authorTags'])
    data['collections'] = len(raw_data['profile']['collections'])
    data['topAuthorTags'] = len(raw_data['profile']['topAuthorTags'])
    data['interestTags'] = len(raw_data['profile']['interestTags'])
    return data


def twitter_parser(file_path):
    data = dict()
    data['twitter_followers'] = ''
    data['twitter_friends'] = ''
    data['twitter_listed'] = ''
    data['twitter_statuses'] = ''
    data['twitter_favourites'] = ''
    data['twitter_description'] = ''
    if file_path == '':
        return data
    with open(file_path, 'r') as f:
        raw_data = json.load(f)
    if 'profile_user' in raw_data:
        raw_data = raw_data['profile_user']
    else:
        return data
    data['twitter_followers'] = raw_data['followers_count']
    data['twitter_friends'] = raw_data['friends_count']
    data['twitter_listed'] = raw_data['listed_count']
    data['twitter_statuses'] = raw_data['statuses_count']
    data['twitter_favourites'] = raw_data['favourites_count']
    if raw_data['description'] == '':
        data['twitter_description'] = 0
    else:
        data['twitter_description'] = 1
    return data
