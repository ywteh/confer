#!/usr/bin/python
import sys, os, operator

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from django.db import connection
from algorithm.utils import *
from db.session import *
from db.entity import *


'''
@author: anant bhardwaj
@date: Feb 12, 2013

script for preparing data in lenskit format
'''


sessions = Session().sessions
entities = Entity().entities
nodes = {}
edges = {}

def load_data():
	cursor = connection.cursor()
	cursor.execute("SELECT auth_no, likes, email1 FROM pcs_authors where likes!= 'NULL' and likes !='[]';")
	data = cursor.fetchall()
	for row in data:
		nodes[row[0]] = {'group': 1, 'name': str(row[2])}
		edges[row[0]] = []
		papers = json.loads(row[1])
		for p in papers:
			name = ""
			if(p in entities):
				name = entities[p]['title'] + '( session: ' + entities[p]['session'] + ')'
			nodes[p] = {'group': 2, 'name': name}	
			edges[row[0]].append(p)



	




def main():
	load_data()
	nodesArray = []
	linksArray = []

	k = 0
	k_papers = 0;
	k_authors = 0;
	for node in nodes:
		y = 0
		nodes[node]['id']= k
		group = nodes[node]['group']
		if(group == 1):
			y = k_authors;
			k_authors = k_authors + 1
		else:
			y = k_papers
			k_papers = k_papers + 1
		nodesArray.append({'name' : nodes[node]['name'], 'group' : group, 'id': k, 'group_id': y})
		k = k + 1

	for edge in edges:
		links = edges[edge]
		s = nodes[edge]['id']
		for l in links:
			linksArray.append({'source' : s, 'target' : nodes[l]['id']})
	
	p = open('data.json','w')
	p.write(json.dumps({"nodes": nodesArray, "links": linksArray}))

if __name__ == '__main__':
    main()
