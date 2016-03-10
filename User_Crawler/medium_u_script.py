# encoding: utf-8
import json
import codecs
import os
import random
import time
import medium_u_crawler_main

def BFS():
	visited = []
	visited_input = codecs.open("./Visited.txt", 'r', 'utf-8')
	visited_list = (str(visited_input.read()).replace('\n','')).split(' ')
	for v in visited_list:
		visited.append(v)
	visited_input.close()
	visited = set(visited)
	queue_input = codecs.open("./Queue.txt", 'r', 'utf-8')
	queue_list = (str(queue_input.read()).replace('\n','')).split(' ')
	queue = set([])
	for q in queue_list:
		if q not in visited:
			queue.add(q)
	queue_input.close()
	while 1:
		if (len(visited)-1) % 30 == 0:
			time.sleep(random.randint(4,7))
			queue_output = codecs.open("./Queue.txt", 'w', 'utf-8')
			for q in queue:
				queue_output.write(str(q) + " ")
			queue_output.close()
			visited_output = codecs.open("./Visited.txt", 'w', 'utf-8')
			for v in visited:
				visited_output.write(str(v) + " ")
			visited_output.close()
		status_output = codecs.open("./Status.txt", 'w', 'utf-8')
		status_output.write("%s users have been visited"%(len(visited)-1))
		status_output.write("%s users are in the Queue"%(len(queue)))
		status_output.close()
		print ("%s users have been visited"%(len(visited)-1))
		print ("%s users are in the Queue"%(len(queue)))
		time.sleep(random.randint(1, 5))
		current = queue.pop()
		if (current == "") or (current in visited):
			continue
		try:
			medium_u_crawler_main.get(current)
		except:
			print("----------Failed")
			continue
		print("----------Success")
		visited.add(current)
		input_text = codecs.open("./Data/%s_following.txt"%str(current), 'r', 'utf-8')
		following = (str(input_text.read()).replace('\n', '').replace('"', '').replace(' ', '').replace("{following_ID:[", "").replace("]}", "")).split(',')
		queue.update(following)
		input_text.close()
		input_text = codecs.open("./Data/%s_followers.txt"%str(current), 'r', 'utf-8')
		followers = (str(input_text.read()).replace('\n', '').replace('"', '').replace(' ', '').replace("{followers_ID:[", "").replace("]}", "")).split(',')
		queue.update(followers)
		input_text.close()

BFS()

