# encoding: utf-8
import random
import time
import json
import codecs
import urllib
import urllib2
import cookielib
import HTMLParser
import re
import get_face_info

class User(object):
    def __init__(self):
        super(User, self).__init__()
        self.data = {
            'ID' : -1,#帐号
            'Name' : -1,#姓名
            'Description' : "",#个人描述
            'Location' : "",#地点
            'JoinDate' : "",#注册时间
            'Tweets' : 0,#推文数量
            'Following' : 0,#关注数量
            'Followers' : 0,#被关注数量
            'Likes' : 0,#点赞数量
            'Avatar' : "",#头像
        }
    
    def getstr(self):
        result = "{\n"\
        + '    \"ID\": \"' + str(self.data['ID']) + "\",\n"\
        + '    \"Name\": \"' + str(self.data['Name']) + "\",\n"\
        + '    \"Description\": \"' + str(self.data['Description']) + "\",\n"\
        + '    \"Location\": \"' + str(self.data['Location']) + "\",\n"\
        + '    \"JoinDate\": \"' + str(self.data['JoinDate']) + "\",\n"\
        + '    \"Tweets\": ' + str(self.data['Tweets']) + ",\n"\
        + '    \"Following\": ' + str(self.data['Following']) + ",\n"\
        + '    \"Followers\": ' + str(self.data['Followers']) + ",\n"\
        + '    \"Likes\": ' + str(self.data['Likes']) + ",\n"\
        + '    \"Avatar\": \"' + str(self.data['Avatar']) + "\"\n}"
        return result

def get_profile(ID):
    url = "https://twitter.com/" + str(ID) + "?lang=en"
    user = User()
    user.data['ID'] = str(ID)

    time.sleep(random.randint(1, 2))
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
          
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2657.0 Safari/537.36')
    response = opener.open(req, timeout=10) 
    data = response.read()

    N = re.findall('ProfileHeaderCard-nameLink u-textInheritColor js-nav\n">(.*?)</a>', data, re.S)
    if len(N)>0:
        user.data['Name'] = N[0]
    
    N = re.findall('nameWithBadges--1\n">(.*?)</a>', data, re.S)
    if len(N)>0:
        user.data['Name'] = N[0]
    
    D = re.findall('<p class="ProfileHeaderCard-bio u-dir"\n      \n      dir="ltr">(.*?)</p>', data, re.S)
    if len(D)>0:
        user.data['Description'] = D[0].replace('"','').replace('/','').replace('<','').replace('>','').replace('\r\n', '').replace('\r', '').replace('\n', '')
    
    L = re.findall('ProfileHeaderCard-locationText u-dir" dir="ltr">\n            (.*?)\n        </span>', data, re.S)
    if len(L)>0:
        user.data['Location'] = L[0].replace('"','').replace('/','').replace('<','').replace('>','').replace('\r\n', '')
    
    J = re.findall('ProfileHeaderCard-joinDateText js-tooltip u-dir" dir="ltr" title="(.*?)">', data, re.S)
    if len(J)>0:
        user.data['JoinDate'] = J[0]
    
    T = re.findall('js-nav" title="(.*?) Tweets" data-nav="tweets"', data, re.S)
    if len(T)>0:
        user.data['Tweets'] = int(T[0].replace(",", ""))
    
    F = re.findall('following">\n        <a class="ProfileNav-stat ProfileNav-stat--link u-borderUserColor u-textCenter js-tooltip js-openSignupDialog js-nonNavigable u-textUserColor" title="(.*?) Following" data-nav="following"', data, re.S)
    if len(F)>0:
        user.data['Following'] = int(F[0].replace(",", ""))
    
    F = re.findall('followers">\n        <a class="ProfileNav-stat ProfileNav-stat--link u-borderUserColor u-textCenter js-tooltip js-openSignupDialog js-nonNavigable u-textUserColor" title="(.*?) Followers" data-nav="followers"', data, re.S)
    if len(F)>0:
        user.data['Followers'] = int(F[0].replace(",", ""))
    
    L = re.findall('favorites">\n        <a class="ProfileNav-stat ProfileNav-stat--link u-borderUserColor u-textCenter js-tooltip js-openSignupDialog js-nonNavigable u-textUserColor" title="(.*?) Likes" data-nav="favorites"', data, re.S)
    if len(L)>0:
        user.data['Likes'] = int(L[0].replace(",", ""))
    
    A = re.findall('<img class="ProfileAvatar-image " src="(.*?)" alt=', data, re.S)
    if len(A)>0:
        user.data['Avatar'] = A[0]
        urllib.urlretrieve(A[0], "./Data/%s_avatar_t.jpg"%str(ID))
        face = get_face_info.get_face_info("./Data/%s_avatar_t.jpg"%str(ID))
        out = codecs.open("./Data/%s_face_t.txt"%str(ID), 'w', 'utf-8')
        out.write(str(face) + "\n")
        out.close()
    
    return user

