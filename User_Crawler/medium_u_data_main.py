# encoding: utf-8
import time
import codecs
import json
import os
import random
import medium_u_profile_crawler
import twitter_u_profile_crawler

def get(ID):
    print (ID)
    try:
        time.sleep(random.randint(1, 2))
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
        ID_input.close()
        Twitter_ID = str(ID_profile['Twitter_ID'])
        print Twitter_ID
        if Twitter_ID != '-1':
            try:
                profile_str = twitter_u_profile_crawler.get_profile(Twitter_ID).getstr()
            except:
                raise
            out = codecs.open("./Data/%s_profile_t.txt"%str(ID), 'w', 'utf-8')
            out.write(profile_str + "\n")
            out.close()
            print("-----Twitter profile obtained")
    except:
        raise

