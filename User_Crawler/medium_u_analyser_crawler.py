# encoding: utf-8
import time
import codecs
import os
import random
import medium_u_profile_crawler
from selenium import webdriver

def get(ID):
	driver = webdriver.Firefox()
	print (ID)
	try:
		time.sleep(random.randint(2, 3))
		profile_str = medium_u_profile_crawler.get_profile(ID, driver).getstr()
		out = codecs.open("./Data/%s_profile.txt"%str(ID), 'w', 'utf-8')
		out.write(profile_str + "\n")
		out.close()
		print("-----profile obtained")
	except:
		driver.quit()
		raise
	driver.quit()
