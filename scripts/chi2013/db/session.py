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

load session
'''


class Session:

	def __init__(self):
		self.sessions = {}
		self.__load__()

	def __load__(self):
		cursor = connection.cursor()
		cursor.execute("SELECT id ,submissions, date, time, room, personas, venue, coreCommunities, title, featuredCommunities, hasAward, hasHonorableMention FROM session WHERE scheduled=1;")
		data = cursor.fetchall()
		for row in data:
			if(row[1]==''):
				submissions = []
			else:
				submissions = [unicode(p).strip().lower() for p in row[1].split(',')]
			id = unicode(row[0]).strip()			
			s_id = unicode(row[0]).strip()
			date = unicode(row[2]).strip()
			t = unicode(row[3]).strip()
			if(t[0]=='9'):
				t = '0'+ t
			room = unicode(row[4]).strip()
			personas = unicode(row[5]).strip()
			venue = unicode(row[6]).strip()
			communities = json.loads(row[7])
			title = unicode(row[8]).strip()	
			award = row[10]
			hm = row[11]			
			self.sessions[id]={'date': date, 'time': t, 'room': room, 'personas': personas, 'communities': communities, 'venue':venue, 's_title':title, 'submissions':submissions, 'award':award, 'hm':hm}


	def get_sessions(self):
		return self.sessions

	

def main():
  s = Session()
  print s.get_sessions()
  

if __name__ == '__main__':
    main()
