#!/usr/bin/python
import os, sys, json, MySQLdb



'''
@author: anant bhardwaj
@date: Feb 12, 2013

load session
'''


class Session:

	def __init__(self):
		self.sessions = {}
		self.__load__()

	def __load__(self):
		connection = MySQLdb.connect(host="mysql.csail.mit.edu",
                     user="cobi",
                      passwd="su4Biha",
                      db="cobi") 
		cursor = connection.cursor()
		cursor.execute("SELECT id ,submissions, date, time, room, personas, venue, coreCommunities, title, featuredCommunities, hasAward, hasHonorableMention FROM session WHERE scheduled=1;")
		data = cursor.fetchall()
		for row in data:
			if(row[1]==''):
				submissions = []
			else:
				submissions = [unicode(p, "ISO-8859-1").strip().lower() for p in row[1].split(',')]
			id = unicode(row[0], "ISO-8859-1").strip()			
			s_id = unicode(row[0], "ISO-8859-1").strip()
			date = unicode(row[2], "ISO-8859-1").strip()
			t = unicode(row[3], "ISO-8859-1").strip()
			if(t[0]=='9'):
				t = '0'+ t
			room = unicode(row[4], "ISO-8859-1").strip()
			personas = unicode(row[5], "ISO-8859-1").strip()
			venue = unicode(row[6], "ISO-8859-1").strip()
			communities = json.loads(row[7])
			title = unicode(row[8], "ISO-8859-1").strip()	
			award = row[10]
			hm = row[11]			
			self.sessions[id]={'day': date, 'time': t, 'room': room, 'personas': personas, 'communities': communities, 'venue':venue, 's_title':title, 'submissions':submissions}


	def get_sessions(self):
		return self.sessions

	

def main():
  s = Session()
  print s.get_sessions()
  

if __name__ == '__main__':
    main()
