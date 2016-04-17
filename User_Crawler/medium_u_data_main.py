# encoding: utf-8
import time
import codecs
import json
import os
import random
import medium_u_profile_crawler

def get(ID):
	print (ID)
	try:
		time.sleep(random.randint(2, 3))
		try:
			profile_str = medium_u_profile_crawler.get_profile(ID).getstr()
		except:
			raise
		out = codecs.open("./Data/%s_profile.txt"%str(ID), 'w', 'utf-8')
		out.write(profile_str + "\n")
		out.close()
		print("-----profile obtained")
		ID_input = open('./Data/%s_profile.txt'%str(ID), 'r')
		ID_profile = json.load(ID_input)
	except:
		raise
