# encoding: utf-8
import time
import codecs
import os
import random
import medium_u_profile_crawler
import medium_u_profile_crawler_s

def get(ID):
	print (ID)
	try:
		profile_str = medium_u_profile_crawler.get_profile(ID).getstr()
	except:
		try:
			profile_str = medium_u_profile_crawler_s.get_profile(ID).getstr()
		except:
			raise
	out = codecs.open("./Data/%s_profile.txt"%str(ID), 'w', 'utf-8')
	out.write(profile_str + "\n")
	out.close()
	print("-----profile obtained")
