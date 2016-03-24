# encoding: utf-8
import random
import time
import json
import codecs
import urllib2
import cookielib
import HTMLParser
import re

class Connection(object):
    def __init__(self):
        super(Connection, self).__init__()
        self.following = []

    def getstr(self):
        result = "{\n    \"following_ID\": \n    [\n"
        if len(self.following) == 0:
            result = result + "    \n    ]\n}"
            return result
        for fol in list(self.following)[:-1]:
            result = result + "        \"" + str(fol) + '\",\n'
        result = result + "        \"" + str(list(self.following)[-1]) + "\"\n    ]\n}"
        return result

def get_following(ID, Num):
    Num = min(300, Num)
    connection = Connection()
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    for i in range(0, Num):
        if (i+1)%40 == 0:
            time.sleep(random.randint(1,2))
        print i
        url = "https://medium.com/@" + str(ID) + "/follow-list?listType=following&page=" + str(i)
        req = urllib2.Request(url)
        req.add_header("User-agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2657.0 Safari/537.36')
        req.add_header("authority", "medium.com")
        req.add_header("method", "GET")
        req.add_header("path", "/@" + str(ID) + "/follow-list?listType=following&page=" + str(i))
        req.add_header("scheme", "https")
        req.add_header("accept", "application/json")
        req.add_header("accept-language", "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4")
        req.add_header("content-type", "application/json")
        req.add_header("referer", "https://medium.com/@" + str(ID))
        req.add_header("x-obvious-cid", "web")
        req.add_header("x-xsrf-token", 1)
        response = opener.open(req, timeout=10)
        data = response.read()
        List = re.findall('"username":"(.*?)"', data, re.S)
        connection.following = connection.following + List

    connection.following = set(connection.following)
    return connection

