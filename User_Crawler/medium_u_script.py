# encoding: utf-8
import json
import os
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
	visited_input = open("./Visited.txt", "r")
	visited_list = (str(visited_input.read()).replace('\n','')).split(' ')
	for v in visited_list:
		visited.append(v)
	visited_input.close()
	queue = Queue()
	queue_input = open("./Queue.txt", "r")
	queue_list = (str(queue_input.read()).replace('\n','')).split(' ')
	for q in queue_list:
		queue.enqueue(q)
	queue_input.close()
	cnt=0
	while queue.size():
		if cnt % 30 == 0:
			queue_output = open("./Queue.txt", "w")
			for q in queue.items:
				queue_output.write(str(q) + " ")
			queue_output.close()
			visited_output = open("./Visited.txt", "w")
			for v in visited:
				visited_output.write(str(v) + " ")
			visited_output.close()
		cnt = cnt + 1
		status_output = open("./Status.txt", "w")
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
		input_text = open("./Data/%s_following.txt"%str(current), "r")
		following = (str(input_text.read()).replace('\n', '').replace('"', '').replace(' ', '').replace("{following_ID:[", "").replace("]}", "")).split(',')
		for fol in following:
			if fol not in visited:
				queue.enqueue(fol)
		input_text.close()
		input_text = open("./Data/%s_followers.txt"%str(current), "r")
		followers = (str(input_text.read()).replace('\n', '').replace('"', '').replace(' ', '').replace("{followers_ID:[", "").replace("]}", "")).split(',')
		for fol in followers:
			if fol not in visited:
				queue.enqueue(fol)
		input_text.close()

BFS()

