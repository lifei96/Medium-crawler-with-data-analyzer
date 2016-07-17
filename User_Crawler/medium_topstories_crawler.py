# encoding: utf-8

import urllib2
import cookielib
import re
import json
import datetime
import codecs
import os


class TopStories(object):
    def __init__(self):
        super(TopStories, self).__init__()
        self.data = {
            'date': "",
            'url': "",
            'num': 0,
            'stories': [],
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
            'date': "",
            'tags': [],
            'recommends': 0,
            'responses': 0,
        }


def get_story(url):
    story = Story()
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent",'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    try:
        response = opener.open(req, timeout=10)
    except urllib2.URLError:
        print('timeout')
        return story
    data = response.read()

    story_id = re.findall('data-post-id="(.*?)" data-is-icon', data)
    if not story_id:
        print('-----fail to get story_id')
    else:
        story.data['story_id'] = story_id[0]

    author = re.findall('"username":"(.*?)","createdAt"', data)
    if not author:
        print('-----fail to get author')
    else:
        story.data['author'] = author[0]

    timestamp = re.findall('"firstPublishedAt":(.*?),"latestPublishedAt"', data)
    if not timestamp:
        print('-----fail to get timestamp')
    else:
        story.data['timestamp'] = float(timestamp[0])
        story.data['date'] = datetime.date.fromtimestamp(story.data['timestamp']/1000.0).isoformat()

    tags = re.findall('false,"tags":(.*?),"socialRecommendsCount"', data)
    if not tags:
        print('-----fail to get tags')
    else:
        story.data['tags'] = json.loads(tags[0])

    recommends = re.findall('"recommends":(.*?),"socialRecommends"', data)
    if not recommends:
        print('-----fail to get recommends')
    else:
        story.data['recommends'] = eval(recommends[0])

    responses = re.findall('"responsesCreatedCount":(.*?),"links"', data)
    if not responses:
        print('-----fail to get responses')
    else:
        story.data['responses'] = eval(responses[0])

    return story


START_DATE = datetime.date(2014, 9, 10)
END_DATE = datetime.date(2016, 7, 16)


def get_top_stories():
    current_date = START_DATE
    while current_date <= END_DATE:
        top_stories = TopStories()
        date_string = current_date.strftime("%B-%d-%Y").lower()
        url = "https://medium.com/browse/top/" + date_string
        top_stories.data['date'] = date_string
        top_stories.data['url'] = url

        cj = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request(url)
        req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/50.0.2661.102 Safari/537.36')
        response = opener.open(req, timeout=10)
        data = response.read()

        stories = []
        story_url = re.findall('<a class="link link--darken" href="(.*?)\?source=top_stories---------[0-9]*-" data-action="open-post"', data)
        num = len(story_url)
        for i in range(num):
            stories.append(get_story(story_url[i]).data)
            print(i)
        top_stories.data['num'] = num
        top_stories.data['stories'] = stories

        out = codecs.open("./TopStories/%s.txt" % current_date.isoformat(), 'w', 'utf-8')
        out.write(top_stories.getstr())
        out.close()
        print("-----%s obtained" % current_date.isoformat())
        current_date = current_date + datetime.timedelta(days=1)

if __name__ == '__main__':
    if not os.path.exists('./TopStories'):
        os.mkdir('./TopStories')
    get_top_stories()
