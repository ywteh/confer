#!/usr/bin/python
import os, sys

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from django.db import connection
from algorithm.utils import *

'''
@author: anant bhardwaj
@date: Feb 12, 2013

load prefs
'''



class Prefs:

	def __init__(self):
		self.author_likes = {}
		self.__load__()


	def __load__(self):
		cursor = connection.cursor()
		cursor.execute("SELECT authorId, id, givenName, familyName FROM authors;")
		data = cursor.fetchall()
		for row in data:
			if(row[0].strip()==''):
				continue
			if(unicode(row[0]).strip() in self.author_likes):
				self.author_likes[unicode(row[0]).strip()]['likes'].append(row[1].strip())
				self.author_likes[unicode(row[0]).strip()]['own_papers'].append(row[1].strip())
			else:
				self.author_likes[unicode(row[0]).strip()] = {'name': unicode(row[2]).strip() + ' ' + unicode(row[3]).strip(), 'likes':[row[1].strip()], 'own_papers':[row[1].strip()]}

		cursor.execute("SELECT authorId, interested FROM authorsourcing;")
		data = cursor.fetchall()
		for row in data:
			if(row[0].strip()==''):
				continue
			likes = [unicode(p).strip() for p in row[1].split(',')]		

			# update author_likes
			if(row[1]!=''):
				self.author_likes[unicode(row[0]).strip()]['likes'].extend(likes)

	


	def get_author_likes(self):
		return self.author_likes

def main():
  p = Prefs()
  print p.get_author_likes()
  #print p.get_paper_prefs()
  

if __name__ == '__main__':
    main()
