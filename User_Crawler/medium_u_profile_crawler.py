# encoding: utf-8
import random
import time
import json
import codecs
import urllib2
import cookielib
import HTMLParser
import re

class User(object):
	def __init__(self):
		super(User, self).__init__()
		self.data = {
			'ID' : -1,#帐号
			'Name' : -1,#姓名
			'Description' : "",#个人描述
			'Following' : 0,#关注数量
			'Followers' : 0,#被关注数量
			'Twitter_ID' : -1,#Twitter帐号
			'Facebook_ID' : -1,#Facebook帐号
		}
	
	def getstr(self):
		result = "{\n"\
		+ '    \"ID\": \"' + str(self.data['ID']) + "\",\n"\
		+ '    \"Name\": \"' + str(self.data['Name']) + "\",\n"\
		+ '    \"Description\": \"' + str(self.data['Description']) + "\",\n"\
		+ '    \"Following\": ' + str(self.data['Following']) + ",\n"\
		+ '    \"Followers\": ' + str(self.data['Followers']) + ",\n"\
		+ '    \"Twitter_ID\": \"' + str(self.data['Twitter_ID']) + "\",\n"\
		+ '    \"Facebook_ID\": \"' + str(self.data['Facebook_ID']) + "\"\n}"
		return result

def get_profile(ID):
	url = "https://medium.com/@" + str(ID)
	user = User()
	user.data['ID'] = str(ID)

	time.sleep(random.randint(2, 3))
	cj = cookielib.MozillaCookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		  
	req = urllib2.Request(url)
	req.add_header("User-agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2657.0 Safari/537.36')
	response = opener.open(req, timeout=10) 
	data = response.read()

	user.data['Name'] = re.findall('title="Go to the profile of (.*?)"', data, re.S)[0]

	user.data['Description'] = re.findall('"hero-description ">(.*?)</p>', data, re.S)[0]

	following = re.findall('title="Show (.*?) people following"', data, re.S)
	if len(following)>0:
		    following = int(filter(str.isdigit, str(following[0])))
	else:
		    following = 0
	user.data['Following'] = following

	followers = re.findall('title="Show (\S+) followers"', data, re.S)
	if len(followers)>0:
		    followers = int(filter(str.isdigit, str(followers[0])))
	else:
		    followers = 0
	user.data['Followers'] = followers

	T = re.findall('twitter.com/(.*?)"', data, re.S)
	if len(T)>0:
		    T = T[0]
	else:
		    T = -1
	user.data['Twitter_ID'] = T

	F = re.findall('facebook.com/(.*?)"', data, re.S)
	if len(F)>0:
		    F = F[0]
	else:
		    F = -1
	user.data['Facebook_ID'] = F

	return user
