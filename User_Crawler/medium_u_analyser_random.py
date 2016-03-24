# encoding: utf-8
from __future__ import division 
import time
import json
import codecs
import os
import random
import medium_u_analyser_crawler

def Get(num):
    Result = ""
    ID_list_input = codecs.open("./ID_list.txt", 'r', 'utf-8')
    ID_list = (str(ID_list_input.read()).replace('\n','')).split(' ')
    ID_list = list(set(ID_list))
    random.shuffle(ID_list)
    ID_list_input.close()
    cnt = 0
    ID_random_list = []
    for ID in ID_list:
        try:
            medium_u_analyser_crawler.get(ID)
        except:
            print("----------Failed")
            continue
        cnt += 1
        print cnt
        ID_random_list.append(ID)
        if cnt >= num:
            break
    ID_profile_list = []
    for ID in ID_random_list:
        ID_input = open('./Data/%s_profile.txt'%str(ID), 'r')
        ID_str = ID_input.read()
        ID_profile = json.loads(str(ID_str))
        ID_profile_list.append(ID_profile)
        ID_input.close()
    Size = len(ID_profile_list)
    Result += "Number of users: %d\n"%Size
    #Only Twitter
    sum_Description = 0
    sum_Following = 0
    sum_Followers = 0
    Sum = 0
    for ID_profile in ID_profile_list:
        if ID_profile["Twitter_ID"] != "-1" and ID_profile["Facebook_ID"] == "-1":
            Sum += 1
            sum_Following += ID_profile["Following"]
            sum_Followers += ID_profile["Followers"]
            if ID_profile["Description"] != "":
                sum_Description += 1
    Result += "Only Twitter:  %d "%Sum
    Result += format((Sum/Size), '.2%')
    if Sum > 0:
        Result += " Description_rate: "
        Result +=  format((sum_Description/Sum), '.2%')
        Result +=  " Following_Avg: %.2f"%(sum_Following/Sum)
        Result +=  " Followers_Avg: %.2f"%(sum_Followers/Sum)
    Result += "\n"
    #Only Facebook
    sum_Description = 0
    sum_Following = 0
    sum_Followers = 0
    Sum = 0
    for ID_profile in ID_profile_list:
        if ID_profile["Twitter_ID"] == "-1" and ID_profile["Facebook_ID"] != "-1":
            Sum += 1
            sum_Following += ID_profile["Following"]
            sum_Followers += ID_profile["Followers"]
            if ID_profile["Description"] != "":
                sum_Description += 1
    Result +=  "Only Facebook: %d "%Sum
    Result +=  format((Sum/Size), '.2%')
    if Sum > 0:
        Result +=  " Description_rate: "
        Result +=  format((sum_Description/Sum), '.2%')
        Result +=  " Following_Avg: %.2f"%(sum_Following/Sum)
        Result +=  " Followers_Avg: %.2f"%(sum_Followers/Sum)
    Result += "\n"
    #Both
    sum_Description = 0
    sum_Following = 0
    sum_Followers = 0
    Sum = 0
    for ID_profile in ID_profile_list:
        if ID_profile["Twitter_ID"] != "-1" and ID_profile["Facebook_ID"] != "-1":
            Sum += 1
            sum_Following += ID_profile["Following"]
            sum_Followers += ID_profile["Followers"]
            if ID_profile["Description"] != "":
                sum_Description += 1
    Result +=  "Both:          %d "%Sum
    Result +=  format((Sum/Size), '.2%')
    if Sum > 0:
        Result +=  " Description_rate: "
        Result +=  format((sum_Description/Sum), '.2%')
        Result +=  " Following_Avg: %.2f"%(sum_Following/Sum)
        Result +=  " Followers_Avg: %.2f"%(sum_Followers/Sum)
    Result += "\n"
    #None
    sum_Description = 0
    sum_Following = 0
    sum_Followers = 0
    Sum = 0
    for ID_profile in ID_profile_list:
        if ID_profile["Twitter_ID"] == "-1" and ID_profile["Facebook_ID"] == "-1":
            Sum += 1
            sum_Following += ID_profile["Following"]
            sum_Followers += ID_profile["Followers"]
            if ID_profile["Description"] != "":
                sum_Description += 1
    Result +=  "None:          %d "%Sum
    Result +=  format((Sum/Size), '.2%')
    if Sum > 0:
        Result +=  " Description_rate: "
        Result +=  format(sum_Description/Sum, '.2%')
        Result +=  " Following_Avg: %.2f"%(sum_Following/Sum)
        Result +=  " Followers_Avg: %.2f"%(sum_Followers/Sum)
    Result += "\n\n"
    return Result

