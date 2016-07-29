# encoding: utf-8

import urllib2
import cookielib
import re
import json
import codecs
import os
import datetime


class User(object):
    def __init__(self):
        super(User, self).__init__()
        self.data = {
            'profile': {},
            'following': [],
            'followers': [],
            'latest': [],
            'recommends': [],
            'highlights': {},
            'responses': [],
        }

    def getstr(self):
        result = json.dumps(self.data, indent=4)
        return result


class Story(object):
    def __init__(self):
        super(Story, self).__init__()
        self.data = {
            'story_id': "",
            'author': "",
            'timestamp': 0,
            'published_date': "",
            'collection': {},
            'tags': [],
            'recommends': 0,
            'responses': 0,
            'response_to': "",
            'success': 1,
        }

    def getstr(self):
        result = json.dumps(self.data, indent=4)
        return result


def get_story(post_id):
    url = 'https://medium.com/posts/' + post_id
    story = Story()
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    try:
        response = opener.open(req, timeout=10)
    except urllib2.URLError:
        story.data['success'] = 0
        print('timeout')
        return story
    data = response.read()

    story_id = re.findall('data-post-id="(.*?)" data-is-icon', data)
    if not story_id:
        story.data['success'] = 0
        print('-----fail to get story_id')
        return story
    else:
        story.data['story_id'] = story_id[0]

    author = re.findall('"username":"(.*?)","createdAt"', data)
    if not author:
        story.data['success'] = 0
        print('-----fail to get author')
        return story
    else:
        story.data['author'] = author[0]

    timestamp = re.findall('"firstPublishedAt":(.*?),"latestPublishedAt"', data)
    if not timestamp:
        story.data['success'] = 0
        print('-----fail to get timestamp')
        return story
    else:
        story.data['timestamp'] = float(timestamp[0])
        story.data['published_date'] = datetime.date.fromtimestamp(story.data['timestamp']/1000.0).isoformat()

    collection = re.findall('"approvedHomeCollection":(.*?),"newsletterId"', data)
    if not collection:
        story.data['collection'] = {}
    else:
        story.data['collection'] = json.loads(collection[0])

    tags = re.findall('false,"tags":(.*?),"socialRecommendsCount"', data)
    if not tags:
        story.data['success'] = 0
        print('-----fail to get tags')
        return story
    else:
        story.data['tags'] = json.loads(tags[0])

    recommends = re.findall('"recommends":(.*?),"socialRecommends"', data)
    if not recommends:
        story.data['success'] = 0
        print('-----fail to get recommends')
        return story
    else:
        story.data['recommends'] = eval(recommends[0])

    responses = re.findall('"responsesCreatedCount":(.*?),"links"', data)
    if not responses:
        story.data['success'] = 0
        print('-----fail to get responses')
        return story
    else:
        story.data['responses'] = eval(responses[0])

    response_to = re.findall('"inResponseToPostId":"(.*?)","inResponseToPost"', data)
    if not response_to:
        story.data['response_to'] = ''
    else:
        story.data['response_to'] = response_to[0]

    return story


def get_following(user_id):
    url = 'https://medium.com/_/api/users/' + user_id + '/following'
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    response = opener.open(req, timeout=10)
    data = response.read()
    following = re.findall('"username":"(.*?)","createdAt"', data)
    following_set = set(following)
    to = re.findall('"to":"(.*?)"}}},"v"', data)
    while to:
        url = 'https://medium.com/_/api/users/' + user_id + '/following?to=' + to[0]
        cj = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request(url)
        req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/50.0.2661.102 Safari/537.36')
        response = opener.open(req, timeout=10)
        data = response.read()
        following = re.findall('"username":"(.*?)","createdAt"', data)
        following_set.update(following)
        to = re.findall('"to":"(.*?)"}}},"v"', data)
    return list(following_set)


def get_followers(user_id):
    url = 'https://medium.com/_/api/users/' + user_id + '/followers'
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    response = opener.open(req, timeout=10)
    data = response.read()
    followers = re.findall('"username":"(.*?)","createdAt"', data)
    followers_set = set(followers)
    to = re.findall('"to":"(.*?)"}}},"v"', data)
    while to:
        url = 'https://medium.com/_/api/users/' + user_id + '/followers?to=' + to[0]
        cj = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request(url)
        req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/50.0.2661.102 Safari/537.36')
        response = opener.open(req, timeout=10)
        data = response.read()
        followers = re.findall('"username":"(.*?)","createdAt"', data)
        followers_set.update(followers)
        to = re.findall('"to":"(.*?)"}}},"v"', data)
    return list(followers_set)


def get_latest(user_id):
    url = 'https://medium.com/_/api/users/' + user_id + '/profile/stream?source=latest'
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    response = opener.open(req, timeout=10)
    data = response.read()
    latest = re.findall('"postId":"(.*?)"},"randomId"', data)
    latest_set = set(latest)
    to = re.findall('"to":"(.*?)","source":"latest"', data)
    while to:
        url = 'https://medium.com/_/api/users/' + user_id + '/profile/stream?source=latest&to=' + to[0]
        cj = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request(url)
        req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/50.0.2661.102 Safari/537.36')
        response = opener.open(req, timeout=10)
        data = response.read()
        latest = re.findall('"postId":"(.*?)"},"randomId"', data)
        latest_set.update(latest)
        to = re.findall('"to":"(.*?)","source":"latest"', data)
    return list(latest_set)


def get_recommends(user_id):
    url = 'https://medium.com/_/api/users/' + user_id + '/profile/stream?source=has-recommended'
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    response = opener.open(req, timeout=10)
    data = response.read()
    recommends = re.findall('w":{"postId":"(.*?)"},"randomId"', data)
    recommends_set = set(recommends)
    to = re.findall('"to":"(.*?)","source":"has-recommended"', data)
    while to:
        url = 'https://medium.com/_/api/users/' + user_id + '/profile/stream?source=has-recommended&to=' + to[0]
        cj = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request(url)
        req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/50.0.2661.102 Safari/537.36')
        response = opener.open(req, timeout=10)
        data = response.read()
        recommends = re.findall('w":{"postId":"(.*?)"},"randomId"', data)
        recommends_set.update(recommends)
        to = re.findall('"to":"(.*?)","source":"has-recommended"', data)
    return list(recommends_set)


def get_highlights(user_id):
    url = 'https://medium.com/_/api/users/' + user_id + '/profile/stream?source=quotes'
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    response = opener.open(req, timeout=10)
    data = response.read()
    highlights = re.findall('{"Quote":(.*?)"type":"Quote"}}', data)
    if not highlights:
        return {}
    highlights_dict = dict(highlights[0] + '"type":"Quote"}}')
    to = re.findall('"to":"(.*?)","source":"quotes"', data)
    while to:
        url = 'https://medium.com/_/api/users/' + user_id + '/profile/stream?source=quotes&to=' + to[0]
        cj = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request(url)
        req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/50.0.2661.102 Safari/537.36')
        response = opener.open(req, timeout=10)
        data = response.read()
        highlights = re.findall('{"Quote":(.*?)"type":"Quote"}}', data)
        if not highlights:
            break
        highlights_dict = highlights_dict.update(dict(highlights[0] + '"type":"Quote"}}'))
        to = re.findall('"to":"(.*?)","source":"quotes"', data)
    return highlights_dict


def get_responses(user_id):
    url = 'https://medium.com/_/api/users/' + user_id + '/profile/stream?source=responses'
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    response = opener.open(req, timeout=10)
    data = response.read()
    responses = re.findall('w":{"postId":"(.*?)"},"randomId"', data)
    responses_set = set(responses)
    to = re.findall('"to":"(.*?)","source":"responses"', data)
    while to:
        url = 'https://medium.com/_/api/users/' + user_id + '/profile/stream?source=responses&to=' + to[0]
        cj = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request(url)
        req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/50.0.2661.102 Safari/537.36')
        response = opener.open(req, timeout=10)
        data = response.read()
        responses = re.findall('w":{"postId":"(.*?)"},"randomId"', data)
        responses_set.update(responses)
        to = re.findall('"to":"(.*?)","source":"responses"', data)
    return list(responses_set)


def post_exist(post):
    return False


def get_posts(user):
    post_list = user.data['latest'] + user.data['recommends'] + user.data['responses']
    highlights = user.data['highlights'].values()
    for quote in highlights:
        post_list.append(quote['postId'])
    post_list = list(set(post_list))
    for post in post_list:
        if not post_exist(post):
            out = codecs.open("./Posts/%s.json" % post, 'w', 'utf-8')
            out.write(get_story(post).getstr())
            out.close()
    for post in user.data['responses']:
        post = get_story(post).data['response_to']
        if post and (not post_exist(post)):
            out = codecs.open("./Posts/%s.json" % post, 'w', 'utf-8')
            out.write(get_story(post).getstr())
            out.close()


def get_user(username):
    if not os.path.exists('./Users'):
        os.mkdir('./Users')
    if not os.path.exists('./Posts'):
        os.mkdir('./Posts')
    print(username)
    user = User()
    url = 'https://medium.com/@' + username
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    try:
        response = opener.open(req, timeout=10)
    except urllib2.URLError:
        print(username + ' timeout')
        return
    data = response.read()

    profile = re.findall('"userMeta":(.*?)"UserMeta"}', data)
    if not profile:
        print('-----fail to get profile')
        return
    else:
        user.data['profile'] = json.loads(profile[0]+'"UserMeta"}')
        print('-----profile')

    user_id = user.data['profile']['user']['userId']

    try:
        user.data['following'] = get_following(user_id)
        print('-----following')
    except:
        print('-----fail to get following')
        return

    try:
        user.data['followers'] = get_followers(user_id)
        print('-----followers')
    except:
        print('-----fail to get followers')
        return

    try:
        user.data['latest'] = get_latest(user_id)
        print('-----latest')
    except:
        print('-----fail to get latest')
        return

    try:
        user.data['recommends'] = get_recommends(user_id)
        print('-----recommends')
    except:
        print('-----fail to get recommends')
        return

    try:
        user.data['highlights'] = get_highlights(user_id)
        print('-----highlights')
    except:
        print('-----fail to get highlights')
        return

    try:
        user.data['responses'] = get_responses(user_id)
        print('-----responses')
    except:
        print('-----fail to get responses')
        return

    try:
        get_posts(user)
        print('-----posts')
    except:
        print('-----fail to get posts')

    out = codecs.open("./Users/%s.json" % username, 'w', 'utf-8')
    out.write(user.getstr())
    out.close()
    print("-----%s obtained" % username)
