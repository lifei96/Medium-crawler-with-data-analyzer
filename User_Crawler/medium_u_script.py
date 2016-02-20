# encoding: utf-8
import json
import codecs
import os
import random
import medium_u_crawler_main

class Queue:
	def __init__(self):
	        self.items = []
	def isEmpty(self): 
		return self.items == [] 
	def enqueue(self, item): 
		self.items.insert(0,item) 
	def dequeue(self): 
		return self.items.pop() 
	def size(self): 
		return len(self.items) 

def BFS():
	visited = []
	visited_input = codecs.open("./Visited.txt", 'r', 'utf-8')
	visited_list = (str(visited_input.read()).replace('\n','')).split(' ')
	for v in visited_list:
		visited.append(v)
	visited_input.close()
	visited = list(set(visited))
	queue = Queue()
	queue_input = codecs.open("./Queue.txt", 'r', 'utf-8')
	queue_list = (str(queue_input.read()).replace('\n','')).split(' ')
	for q in queue_list:
		if q not in visited:
			queue.enqueue(q)
	queue_input.close()
	queue.items = list(set(queue.items))
	random.shuffle(queue.items)
	while queue.size():
		if (len(visited)-1) % 100 == 0:
			queue_output = codecs.open("./Queue.txt", 'w', 'utf-8')
			for q in queue.items:
				queue_output.write(str(q) + " ")
			queue_output.close()
			visited_output = codecs.open("./Visited.txt", 'w', 'utf-8')
			for v in visited:
				visited_output.write(str(v) + " ")
			visited_output.close()
			random.shuffle(queue.items)
		status_output = codecs.open("./Status.txt", 'w', 'utf-8')
		status_output.write("%s users have been visited"%(len(visited)-1))
		status_output.write("%s users are in the Queue"%(queue.size()))
		status_output.close()
		print ("%s users have been visited"%(len(visited)-1))
		print ("%s users are in the Queue"%(queue.size()))
		current = queue.dequeue()
		if current == "":
			continue
		try:
			medium_u_crawler_main.get(current)
		except:
			print("----------Failed")
			continue
		print("----------Success")
		visited.append(current)
		input_text = codecs.open("./Data/%s_following.txt"%str(current), 'r', 'utf-8')
		following = (str(input_text.read()).replace('\n', '').replace('"', '').replace(' ', '').replace("{following_ID:[", "").replace("]}", "")).split(',')
		for fol in following:
			if fol not in visited:
				if fol not in queue.items:
					queue.enqueue(fol)
		input_text.close()
		input_text = codecs.open("./Data/%s_followers.txt"%str(current), 'r', 'utf-8')
		followers = (str(input_text.read()).replace('\n', '').replace('"', '').replace(' ', '').replace("{followers_ID:[", "").replace("]}", "")).split(',')
		for fol in followers:
			if fol not in visited:
				if fol not in queue.items:
					queue.enqueue(fol)
		input_text.close()

BFS()

