# encoding: utf-8
from __future__ import division 
import time
import json
import codecs
import os
import random

def Get(Lim):
    m_num = [0, 0, 0, 0]
    m_bio = [0, 0, 0, 0]
    m_fing = [0, 0, 0, 0]
    m_fers = [0, 0, 0, 0]
    m_ava = [0, 0, 0, 0]
    m_pub = [0, 0, 0, 0]
    t_bio = [0, 0, 0, 0]
    t_t = [0, 0, 0, 0]
    t_fing = [0, 0, 0, 0]
    t_fers = [0, 0, 0, 0]
    t_like = [0, 0, 0, 0]
    Result = ""
    ID_visited_input = codecs.open("./ID_visited.txt", 'r', 'utf-8')
    ID_v = (str(ID_visited_input.read()).replace('\n','')).split(' ')
    ID_v = list(set(ID_v))
    random.shuffle(ID_v)
    ID_visited_input.close()
    Num = 0
    for ID in ID_v:
        try:
            ID_m_input = open('./Data/%s_profile.txt'%str(ID), 'r')
            ID_m_str = ID_m_input.read()
            ID_m_profile = json.loads(str(ID_m_str))
            ID_m_input.close()
            if ID_m_profile['Twitter_ID'] != '-1':
                ID_t_input = open('./Data/%s_profile_t.txt'%str(ID), 'r')
                ID_t_str = ID_t_input.read()
                ID_t_profile = json.loads(str(ID_t_str))
                ID_t_input.close()
            #Neither
            if ((ID_m_profile['Twitter_ID'] == '-1') and (ID_m_profile['Facebook_ID'] == '-1')):
                m_num[0] = m_num[0] + 1
                if ID_m_profile['Description'] != '':
                    m_bio[0] = m_bio[0] + 1
                m_fing[0] = m_fing[0] + ID_m_profile['Following']
                m_fers[0] = m_fers[0] + ID_m_profile['Followers']
                if ID_m_profile['Avatar'] != '':
                    m_ava[0] = m_ava[0] + 1
                if ID_m_profile['Publications'] == '1':
                    m_pub[0] = m_pub[0] + 1
            #Only Facebook
            if ((ID_m_profile['Twitter_ID'] == '-1') and (ID_m_profile['Facebook_ID'] != '-1')):
                m_num[1] = m_num[1] + 1
                if ID_m_profile['Description'] != '':
                    m_bio[1] = m_bio[1] + 1
                m_fing[1] = m_fing[1] + ID_m_profile['Following']
                m_fers[1] = m_fers[1] + ID_m_profile['Followers']
                if ID_m_profile['Avatar'] != '':
                    m_ava[1] = m_ava[1] + 1
                if ID_m_profile['Publications'] == '1':
                    m_pub[1] = m_pub[1] + 1
            #Only Twitter
            if ((ID_m_profile['Twitter_ID'] != '-1') and (ID_m_profile['Facebook_ID'] == '-1')):
                m_num[2] = m_num[2] + 1
                if ID_m_profile['Description'] != '':
                    m_bio[2] = m_bio[2] + 1
                m_fing[2] = m_fing[2] + ID_m_profile['Following']
                m_fers[2] = m_fers[2] + ID_m_profile['Followers']
                if ID_m_profile['Avatar'] != '':
                    m_ava[2] = m_ava[2] + 1
                if ID_m_profile['Publications'] == '1':
                    m_pub[2] = m_pub[2] + 1
                if ID_t_profile['Description'] != '':
                    t_bio[2] = t_bio[2] + 1
                t_t[2] = t_t[2] + ID_t_profile['Tweets']
                t_fing[2] = t_fing[2] + ID_t_profile['Following']
                t_fers[2] = t_fers[2] + ID_t_profile['Followers']
                t_like[2] = t_like[2] + ID_t_profile['Likes']
            #Both
            if ((ID_m_profile['Twitter_ID'] != '-1') and (ID_m_profile['Facebook_ID'] != '-1')):
                m_num[3] = m_num[3] + 1
                if ID_m_profile['Description'] != '':
                    m_bio[3] = m_bio[3] + 1
                m_fing[3] = m_fing[3] + ID_m_profile['Following']
                m_fers[3] = m_fers[3] + ID_m_profile['Followers']
                if ID_m_profile['Avatar'] != '':
                    m_ava[3] = m_ava[3] + 1
                if ID_m_profile['Publications'] == '1':
                    m_pub[3] = m_pub[3] + 1
                if ID_t_profile['Description'] != '':
                    t_bio[3] = t_bio[3] + 1
                t_t[3] = t_t[3] + ID_t_profile['Tweets']
                t_fing[3] = t_fing[3] + ID_t_profile['Following']
                t_fers[3] = t_fers[3] + ID_t_profile['Followers']
                t_like[3] = t_like[3] + ID_t_profile['Likes']
        except:
            print(ID)
            print('-----Failed')
            continue
        Num = Num + 1
        if Num >= Lim:
            print(Num)
            print(Lim)
            break
    
    Result = 'Number of users: %d\n'%Num
    for i in range(4):
        if i == 0:
            Result = Result + '\n' + '-----Neither' 
        if i == 1:
            Result = Result + '\n' + '-----Only Facebook' 
        if i == 2:
            Result = Result + '\n' + '-----Only Twitter' 
        if i == 3:
            Result = Result + '\n' + '-----Both' 
        Result = Result + ' %d '%m_num[i] + format((m_num[i]/Num), '.2%') + '\n'
        Result = Result + 'Bio_rate: ' + format((m_bio[i]/m_num[i]), '.2%') + '\n'
        Result = Result + 'Following_avg: %.2f'%(m_fing[i]/m_num[i]) + '\n'
        Result = Result + 'Followers_avg: %.2f'%(m_fers[i]/m_num[i]) + '\n'
        Result = Result + 'Avatar_rate: ' + format((m_ava[i]/m_num[i]), '.2%') + '\n'
        Result = Result + 'Publication_rate: ' + format((m_pub[i]/m_num[i]), '.2%') + '\n'
        if i > 1:
            Result = Result + '---Twitter Data---' + '\n'
            Result = Result + 'T_Bio_rate: ' + format((t_bio[i]/m_num[i]), '.2%') + '\n'
            Result = Result + 'T_Tweets_avg: %.2f'%(t_t[i]/m_num[i]) + '\n'
            Result = Result + 'T_Following_avg: %.2f'%(t_fing[i]/m_num[i]) + '\n'
            Result = Result + 'T_Followers_avg: %.2f'%(t_fers[i]/m_num[i]) + '\n'
            Result = Result + 'T_Likes_avg: %.2f'%(t_like[i]/m_num[i]) + '\n'
    
    out = codecs.open("./Result_%d.txt"%Num, 'w', 'utf-8')
    out.write(Result + "\n")
    out.close()

Get(300)
