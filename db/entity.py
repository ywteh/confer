#!/usr/bin/python
import os, sys, json


if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
from django.db import connection

'''
@author: anant bhardwaj
@date: Feb 12, 2013

load entities
'''


class Entity:

	def __init__(self):
		self.entities = {}
		self.__load__()

	def __load__(self):
		cursor = connection.cursor()
		cursor.execute("SELECT id , authors, title, cAndB, keywords, abstract, session, bestPaperAward, bestPaperNominee, coreCommunities, subtype FROM entity;")
		data = cursor.fetchall()
		for row in data:
			if(row[0]!=''):
				authors = json.loads(unicode(row[1]).strip())
				title = unicode(row[2]).strip()
				c_and_b = unicode(row[3]).strip('"')
				keywords = unicode(row[4]).strip('"')
				abstract = unicode(row[5]).strip('"')
				session = unicode(row[6]).strip('"')
				award = row[7]
				hm = row[8]
				communities = json.loads(row[9])
				subtype = row[10]
				self.entities[row[0]]={'authors': authors, 'title': title, 'c_and_b': c_and_b, 'keywords': keywords, 'abstract':abstract, 'session': session, 'award':award, 'hm':hm, 'communities': communities, 'subtype':subtype}


	def get_entities(self):
		return self.entities

	

def main():
  e = Entity()
  print e.get_entities()
  

if __name__ == '__main__':
    main()
