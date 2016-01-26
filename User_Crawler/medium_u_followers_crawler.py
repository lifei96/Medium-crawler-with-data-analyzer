# encoding: utf-8
import random
import time
from selenium import webdriver

class Connection(object):
	def __init__(self):
		super(Connection, self).__init__()
		self.followers = []

	def getstr(self):
		result = "{\n    \"followers_ID\": \n    [\n"
		if len(self.followers) == 0:
			result = result + "    \n    ]\n}"
			return result
		for fol in list(self.followers)[:-1]:
			result = result + "        \"" + str(fol) + '\",\n'
		result = result + "        \"" + str(list(self.followers)[-1]) + "\"\n    ]\n}"
		return result

def get_followers(ID, driver):
	url = "https://medium.com/@" + str(ID)
	driver.get(url)
	time.sleep(3)
	connection = Connection()
	flag = 0
	button_list = driver.find_elements_by_class_name("button")
	for button in button_list:
		if button.get_attribute("data-action-value") == "followers":
			button.click()
			time.sleep(2)
			flag = 1
			break
	if flag == 0:
		return connection
	size=0
	cnt=0
	cnt2=0
	while True:
		cnt2 = cnt2 + 1
		if cnt2 % 10 == 0:
			cnt = 0
		flag = 0
		button_list = driver.find_elements_by_class_name("button")
		for button in button_list:
			if button.get_attribute("data-action") == "load-more-follows":
				try:
					button.click()
				except:
					break
				time.sleep(2)
				flag = 1
				break
		if flag == 0:
			cnt = cnt + 1
			if cnt > 5:
				break
		followers_list = driver.find_elements_by_class_name("link")
		if(len(followers_list) > size):
			size = len(followers_list)
		else:
			cnt = cnt + 1
			if cnt > 5:
				break
	print (len(followers_list))
	cnt = 0
	for fol in followers_list:
		if fol.get_attribute("data-action") == "show-user-card":
			cnt = cnt + 1
			if cnt % 2 == 1:
				if str(fol.get_attribute("href"))[20:] != str(ID):
					connection.followers = connection.followers + [str(fol.get_attribute("href"))[20:]]
	connection.followers = set(connection.followers)
	return connection
	
