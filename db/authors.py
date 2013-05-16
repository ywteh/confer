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

load authors
'''



class Authors:

	def __init__(self):
		self.authors = {}
		self.__load__()


	def __load__(self):
		cursor = connection.cursor()
		cursor.execute("SELECT id, email1, given_name, family_name, instituition1 FROM pcs_authors;")
		data = cursor.fetchall()
		for row in data:
			if(row[2].strip()!=""):			
				self.authors[row[0].strip()] = {'email': unicode(row[1]).strip(), 'name': unicode(row[2]).strip() +  ' ' + unicode(row[3]).strip(), 'institution': unicode(row[4]).strip()}
	

	def get_authors(self):
		return self.authors

def main():
  a = Authors()
  print a.get_authors()
  
  

if __name__ == '__main__':
    main()
