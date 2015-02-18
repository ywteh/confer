#!/usr/bin/python
import sys, os
import ast

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from django.db import connection


'''
@author: anant bhardwaj
@date: Feb 12, 2013

script for preparing data in lenskit format
'''



def dump_log():
	cursor = connection.cursor()
	cursor.execute("SELECT * from logs")
	data = cursor.fetchall()
	for row in data:
		reg_id =  row[2]
		action = row[3]
		vals = []
		if row[4].strip() != '':
			vals = ast.literal_eval(str(row[4]))
		
		if action == 'star':
			for d in vals:
				print "UPDATE likes SET likes.likes = array_append(likes.likes, '%s') WHERE reg_id=%s AND likes.likes@>ARRAY['%s']" %(d, reg_id, d)
				print "SELECT likes.likes FROM likes WHERE reg_id='%s'" %(reg_id)
		elif action == 'unstar':
			for d in vals:
				print "UPDATE likes SET likes.likes = array_remove(likes.likes, '%s') WHERE reg_id=%s AND likes.likes@>ARRAY['%s']" %(d, reg_id, d)
				print "SELECT likes.likes FROM likes WHERE reg_id='%s'" %(reg_id)
		elif action == 'papers':
			print "SELECT papers::json FROM conferences WHERE conf_id='?'"
			print "SELECT likes.likes FROM likes WHERE reg_id='%s'" %(reg_id)
		elif action == 'schedule':
			print "SELECT schedule::json FROM conferences WHERE conf_id='?'"
			print "SELECT likes.likes FROM likes WHERE reg_id='%s'" %(reg_id)
		elif action == 'selected_paper':
			print "SELECT papers::json->>'?' FROM conferences WHERE conf_id='?'"
			print "SELECT likes.likes FROM likes WHERE reg_id='%s'" %(reg_id)
		elif action == 'similar_people':
			print "SELECT likes.likes FROM likes WHERE reg_id='%s'" %(reg_id)
			print "SELECT users FROM registrations WHERE conf_id='?'"
		else:
			print action

	




def main():
	dump_log()

if __name__ == '__main__':
    main()
