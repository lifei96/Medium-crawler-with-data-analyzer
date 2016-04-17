# encoding: utf-8
import json
import codecs
import os
import random
import time
import gc

visited = []
visited_input = codecs.open("./Visited.txt", 'r', 'utf-8')
visited_list = (str(visited_input.read()).replace('\n','')).split(' ')
for v in visited_list:
    visited.append(v)
visited_input.close()
visited = set(visited)
del visited_list
gc.collect()
queue_input = codecs.open("./Queue.txt", 'r', 'utf-8')
queue_list = (str(queue_input.read()).replace('\n','')).split(' ')
queue = set([])
for q in queue_list:
    if q not in visited:
        queue.add(q)
queue_input.close()
del queue_list
gc.collect()
ID_list = visited | queue
ID_list_output = codecs.open("./ID_list.txt", 'w', 'utf-8')
for i in ID_list:
    ID_list_output.write(str(i) + " ")
ID_list_output.close()

