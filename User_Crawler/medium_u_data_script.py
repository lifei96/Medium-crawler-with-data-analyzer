# encoding: utf-8
import json
import codecs
import os
import random
import time
import medium_u_data_main
import gc

def Get():
    visited = []
    visited_input = codecs.open("./ID_visited.txt", 'r', 'utf-8')
    visited_list = (str(visited_input.read()).replace('\n','')).split(' ')
    for v in visited_list:
        visited.append(v)
    visited_input.close()
    visited = set(visited)
    del visited_list
    gc.collect()
    queue_input = codecs.open("./ID_list.txt", 'r', 'utf-8')
    queue_list = (str(queue_input.read()).replace('\n','')).split(' ')
    queue = []
    for i in range(5):
        random.shuffle(queue_list)
    for q in queue_list:
        if q not in visited:
            queue.append(q)
    queue_input.close()
    del queue_list
    gc.collect()
    while len(queue):
        if (len(visited)-1) % 100 == 0:
            time.sleep(random.randint(4,7))
            queue_output = codecs.open("./ID_list.txt", 'w', 'utf-8')
            for q in queue:
                queue_output.write(str(q) + " ")
            queue_output.close()
            visited_output = codecs.open("./ID_visited.txt", 'w', 'utf-8')
            for v in visited:
                visited_output.write(str(v) + " ")
            visited_output.close()
        status_output = codecs.open("./ID_status.txt", 'w', 'utf-8')
        status_output.write("%s users have been ID_visited"%(len(visited)-1))
        status_output.write("%s users are in the ID_list"%(len(queue)))
        status_output.close()
        print ("%s users have been ID_visited"%(len(visited)-1))
        print ("%s users are in the ID_list"%(len(queue)))
        time.sleep(random.randint(1, 3))
        current = queue[0]
        queue.remove(current)
        if os.path.exists('./Data/%s_profile.txt'%str(current)):
            visited.add(current)
        if (current == "") or (current in visited):
            continue
        try:
            medium_u_data_main.get(current)
        except:
            print("----------Failed")
            continue
        print("----------Success")
        visited.add(current)

Get()

