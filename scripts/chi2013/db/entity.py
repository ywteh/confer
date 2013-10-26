#!/usr/bin/python
import os, sys, json, MySQLdb

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
		connection = MySQLdb.connect(host="mysql.csail.mit.edu",
                     user="cobi",
                      passwd="su4Biha",
                      db="cobi") 
		cursor = connection.cursor()
		cursor.execute("SELECT id , authors, title, cAndB, keywords, abstract, session, bestPaperAward, bestPaperNominee, coreCommunities, subtype FROM entity;")
		data = cursor.fetchall()
		cursor.close()
		for row in data:
			if(row[0]!=''):
				authors = []
				authors_list = json.loads(unicode(row[1], "ISO-8859-1").strip())

				for author in authors_list:
					print author
					institution = ''
					if 'primary' in author and author['primary']:
						if 'institution' in  author['primary']:
							institution =  author['primary']['institution']
						else:
							institution = author['primary']['dept']

					email = ''
					if 'email' in author and author['email']:
						email = author['email']

					authors.append({
						'name': author['givenName'] + ' ' + author['familyName'],
						'affiliation': institution,
						'email': email
						})

				title = unicode(row[2], "ISO-8859-1").strip()
				c_and_b = unicode(row[3], "ISO-8859-1").strip('"')
				keywords = unicode(row[4], "ISO-8859-1").strip('"')
				abstract = unicode(row[5], "ISO-8859-1").strip('"')
				session = unicode(row[6], "ISO-8859-1").strip('"')
				award = row[7]
				hm = row[8]
				communities = json.loads(row[9])
				subtype = row[10]
				self.entities[row[0]]={'authors': authors, 'title': title, 'c_and_b': c_and_b, 'keywords': keywords, 'abstract':abstract, 'award':award, 'hm':hm, 'communities': communities, 'subtype':subtype}


	def get_entities(self):
		return self.entities

	

def main():
  e = Entity()
  print e.get_entities()
  

if __name__ == '__main__':
    main()
