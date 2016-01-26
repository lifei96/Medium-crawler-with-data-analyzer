# encoding: utf-8
import json
import codecs
import os
import medium_u_crawler_main

begin_ID = "chenyang03"

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
        
def BFS(start):
	visited = []
	queue = Queue()
	queue.enqueue(start)
	while queue.size():
		current = queue.dequeue()
		visited.append(current)
		medium_u_crawler_main.get(current)
		input_text = codecs.open("./Data/%s_following.txt"%str(current), 'r', 'utf-8')
		following = (str(input_text.read()).replace('\n', '').replace('"', '').replace(' ', '').replace("{following_ID:[", "").replace("]}", "")).split(',')
		for fol in following:
			if fol not in visited:
				queue.enqueue(fol)
		input_text.close()
		input_text = codecs.open("./Data/%s_followers.txt"%str(current), 'r', 'utf-8')
		followers = (str(input_text.read()).replace('\n', '').replace('"', '').replace(' ', '').replace("{followers_ID:[", "").replace("]}", "")).split(',')
		for fol in followers:
			if fol not in visited:
				queue.enqueue(fol)
		input_text.close()

BFS(begin_ID)

