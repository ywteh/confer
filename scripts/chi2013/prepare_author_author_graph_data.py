#!/usr/bin/python
import sys, os, operator, numpy
import matplotlib.pyplot as plt

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from django.db import connection
from algorithm.utils import *
from db.session import *
from db.entity import *
from collections import defaultdict


'''
@author: anant bhardwaj
@date: Feb 12, 2013

script for preparing data in lenskit format
'''


sessions = Session().sessions
entities = Entity().entities
nodes = {}
edges = defaultdict(dict)
likes = defaultdict(set)


papers_count = [];

def load_data():
	cursor = connection.cursor()
	cursor.execute("SELECT auth_no, likes, email1 FROM pcs_authors where likes!= 'NULL' and likes !='[]';")
	data = cursor.fetchall()
	for row in data:
		papers = set(json.loads(row[1]))
		nodes[row[0]] = {'papers': papers}

	for p1 in nodes:
		for p2 in nodes:			
			common_likes = nodes[p1]['papers'].intersection(nodes[p2]['papers'])				
			edges[p1][p2] = len(common_likes)



def main():
	load_data()
	nodesArray = []
	linksArray = []
	
	
	

	
	
	
	k = 0

	for node in nodes:
		nodesArray.append({'title' : '', 'session': '', 'weight': 30})
		nodes[node]['id']= k
		k = k+1
	
	
	edgesToRemove = set()
	'''
	for edge in edges:
		links = edges[edge]
		for l in links:
			weight = edges[edge][l]
			if(weight > 14):
				edgesToRemove.add(nodes[edge]['id'])
				edgesToRemove.add(nodes[l]['id'])
	'''

	for edge in edges:
		links = edges[edge]
		for l in links:
			weight = edges[edge][l]
			if(weight > 20 and (nodes[edge]['id'] not in edgesToRemove) and (nodes[l]['id'] not in edgesToRemove)):
				linksArray.append({'source' : nodes[edge]['id'], 'target' : nodes[l]['id'], 'weight': weight})
	
	p = open('/Volumes/Workspace/www/data.json','w')
	p.write(json.dumps({"nodes": nodesArray, "links": linksArray}))

	

if __name__ == '__main__':
    main()
