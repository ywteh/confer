#!/usr/bin/python
import os, sys, MySQLdb

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
		connection = MySQLdb.connect(host="mysql.csail.mit.edu",
                     user="cobi",
                      passwd="su4Biha",
                      db="cobi") 
		cursor = connection.cursor()
		cursor.execute("SELECT id, email1, given_name, family_name, instituition1 FROM pcs_authors;")
		data = cursor.fetchall()
		cursor.close()
		for row in data:
			if row[2] and row[2].strip()!="":			
				self.authors[row[0].strip()] = {'email': unicode(row[1], "ISO-8859-1").strip(), 'name': unicode(row[2],"ISO-8859-1").strip() +  ' ' + unicode(row[3], "ISO-8859-1").strip(), 'institution': unicode(row[4], "ISO-8859-1").strip()}
	

	def get_authors(self):
		return self.authors

def main():
  a = Authors()
  print a.get_authors()
  
  

if __name__ == '__main__':
    main()
