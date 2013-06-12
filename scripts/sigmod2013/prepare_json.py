import sys, os, json, csv, re

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/../..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/../.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")



def prepare_paper_json():
	f = open('data/sigmod2013/prog_ck.csv','rU')
	reader = csv.reader(f)
	papers = {}
	header= True
	paper_id = None
	for row in reader:
		if(header or len(row)==0):
			header = False
		else:
			if(row[1] != ''):
				authors = []				
				session = unicode(row[0], "ISO-8859-1")
				if(row[1].startswith('sig')):
					paper_id = 'sig'+re.search(r'\d+', row[1]).group()
				elif(row[1].startswith('pods')):
					paper_id = 'pods'+re.search(r'\d+', row[1]).group()
				else:
					paper_id = row[1]
				title = unicode(row[2], "ISO-8859-1")
				subtitle = unicode(row[3], "ISO-8859-1")
				num_pages = unicode(row[4], "ISO-8859-1")
				abstract = unicode(row[5], "ISO-8859-1")
				authors.append(
					{'name': unicode(row[6], "ISO-8859-1") + ' ' + unicode(row[8], "ISO-8859-1"), 
					'email': unicode(row[8], "ISO-8859-1"), 
					'affiliation': unicode(row[10], "ISO-8859-1"), 
					'location': unicode(row[11], "ISO-8859-1")}
					)
				papers[paper_id]={'authors': authors, 'title': title, 'abstract':abstract, 'session': session}
			else:
				papers[paper_id]['authors'].append(
					{'name': unicode(row[6], "ISO-8859-1") + ' ' + unicode(row[8], "ISO-8859-1"), 
					'email': unicode(row[8], "ISO-8859-1"), 
					'affiliation': unicode(row[10], "ISO-8859-1"), 
					'location': unicode(row[11], "ISO-8859-1")}
					)
		p = open('server/static/json/sigmod2013/papers.json','w')
		p.write('entities='+json.dumps(papers))


def prepare_session_json():
	f = open('data/sigmod2013/s_research.csv','rU')
	reader = csv.reader(f)
	sessions = {}
	header= True
	session_id = None
	for row in reader:
		if(header or len(row)==0):
			header = False
		else:
			if(row[1]!='' and row[2]!=''):
				submissions = []
				session_id = 'Research ' + row[1]
				s_title = unicode(row[2], "ISO-8859-1")
				submissions.append('sig%03d' %(int(row[3])))
				sessions[session_id]={'s_title': s_title, 'submissions':submissions}
			else:
				if(session_id != None and row[3]!=''):
					sessions[session_id]['submissions'].append('sig%03d' %(int(row[3])))
	f = open('data/sigmod2013/s_industrial.csv','rU')
	reader = csv.reader(f)
	header= True
	session_id = None
	for row in reader:
		if(header or len(row)==0):
			header = False
		else:
			if(row[1]!='' and row[2] == '' and row[0]==''):
				submissions = []
				session_id = row[1][:row[1].index(':')]
				s_title = unicode(row[1], "ISO-8859-1").strip()
				sessions[session_id]={'s_title': s_title, 'submissions':submissions}
			else:
				if(session_id != None and row[1]!='' and row[2]!=''):
					sessions[session_id]['submissions'].append('sig%03d' %(int(row[0])))
	f = open('data/sigmod2013/s_demo.csv','rU')
	reader = csv.reader(f)
	header= True
	session_id = None
	for row in reader:
		if(header or len(row)==0):
			header = False
		else:
			if(row[1]!='' and row[2] == '' and row[0]==''):
				submissions = []
				session_id = row[1][:row[1].index(':')]
				s_title = unicode(row[1], "ISO-8859-1").strip()
				sessions[session_id]={'s_title': s_title, 'submissions':submissions}
			else:
				if(session_id != None and row[1]!='' and row[2]!=''):
					sessions[session_id]['submissions'].append('sig%03d' %(int(row[0])))
	f = open('data/sigmod2013/s_tutorial.csv','rU')
	reader = csv.reader(f)
	header= True
	session_id = None
	for row in reader:
		if(header or len(row)==0):
			header = False
		else:
			if(row[1]!=''):
				submissions = []
				session_id = row[1][:row[1].index(':')]
				s_title = unicode(row[1], "ISO-8859-1").strip()
				submissions.append('sig%03d' %(int(row[0])))
				sessions[session_id]={'s_title': s_title, 'submissions':submissions}
	
	p = open('server/static/json/sigmod2013/sessions.json','w')
	p.write('sessions='+json.dumps(sessions))
	
		#print sessions



def prepare_schedule_json():	
	schedule = [
	{
	'day': 'Tuesday', 
	'date':'06/25/2013', 
	'slots':[
		{'time':'10:30-12:30', 
			'sessions':
				[
				{'session':'PODS 5', 'room':'3.04/3.05'},
				{'session':'Research 1',  'room':'3.11'},
				{'session':'Research 2',  'room':'4.04/4.05'},
				{'session':'Research 3',  'room':'Times Sq.'},
				{'session':'Tutorial 1',  'room':'4.02/4.03'},
				{'session':'Industry 1',  'room':'Hudson'},
				{'session':'Demo 1', 'room':'Manhattan'},
				]
		},
		{'time':'13:30-15:00',
		'sessions':[	
				{'session':'PODS 6', 'room':'3.04/3.05'},
				{'session':'Research 4', 'room':'3.11'},
				{'session':'Research 5', 'room':'4.04/4.05'},
				{'session':'Research 6', 'room':'Times Sq.'},
				{'session':'Tutorial 2', 'room':'4.02/4.03'},
				{'session':'Industry 2', 'room':'Hudson'},
				{'session':'Demo 2', 'room':'Manhattan'},
				]
		},
		{'time':'15:30-17:00',
		'sessions':
				[
				{'session':'PODS 7', 'room':'3.04/3.05'},
				{'session':'Research 7', 'room':'3.11'},
				{'session':'Research 9', 'room':'4.04/4.05'},
				{'session':'Research 8', 'room':'Times Sq.'},
				{'session':'Tutorial 2', 'room':'4.02/4.03'},
				{'session':'Industry 3', 'room':'Hudson'},
				{'session':'Demo 3', 'room':'Manhattan'},
				]
		}
	]
			
	},
	{
	'day': 'Wednesday',
	'date':'06/26/2013',
	'slots':[
		{'time':'10:30-12:30',
		'sessions':
			[
			{'session':'PODS 8', 'room':'3.04/3.05'},
			{'session':'Research 10', 'room':'3.11'},
			{'session':'Research 11', 'room':'4.04/4.05'},
			{'session':'Research 12', 'room':'Times Sq.'},
			{'session':'Tutorial 3',  'room':'4.02/4.03'},
			{'session':'Industry 4', 'room':'Hudson'},
			{'session':'Demo 4', 'room':'Manhattan'},
			]
		},
		{
		'time':'16:00-17:30',
		'sessions':
			[
			{'session':'PODS 9', 'room':'3.04/3.05'},
			{'session':'Research 13', 'room':'3.11'},
			{'session':'Research 15', 'room':'4.04/4.05'},
			{'session':'Research 14', 'room':'Times Sq.'},
			{'session':'Tutorial 3', 'room':'4.02/4.03'},
			{'session':'Demo 1', 'room':'Hudson'},
			{'session':'Panel', 'room':'Manhattan'},
			]
		}

	]

	},


	{
	'day': 'Thursday', 
	'date':'06/27/2013',
	'slots':[
		{'time':'10:30-12:30',
		'sessions':
			[
			{'session':'Research 16', 'room':'3.04/3.05'},
			{'session':'Research 17', 'room':'3.11'},
			{'session':'Research 18', 'room':'Times Sq.'},
			{'session':'Tutorial 4', 'room':'4.02/4.03'},
			{'session':'Industry 5', 'room':'Hudson'},
			{'session':'Demo 2', 'room':'Manhattan'},
			]
		},

		{'time':'13:30-15:00',
		'sessions':
			[
			{'session':'Research 19', 'room':'3.11'},
			{'session':'Research 20', 'room':'4.04/4.05'},
			{'session':'Research 21', 'room':'Times Sq.'},
			{'session':'Research 22', 'room':'Hudson'},
			{'session':'Tutorial 5', 'room':'4.02/4.03'},	
			{'session':'Demo 3', 'room':'Manhattan'},
			]
		},
		{'time':'15:30-17:00',
		'sessions':
			[
			{'session':'Research 23', 'room':'3.11'},
			{'session':'Research 24', 'room':'4.04/4.05'},
			{'session':'Research 26', 'room':'Times Sq.'},
			{'session':'Research 25', 'room':'Hudson'},
			{'session':'Tutorial 6', 'room':'4.02/4.03'},	
			{'session':'Demo 4', 'room':'Manhattan'}
			]
		}
	]
	}
	]
	p = open('server/static/json/sigmod2013/schedule.json','w')
	p.write('schedule='+json.dumps(schedule))

def main():
	prepare_paper_json()
	prepare_session_json()
	prepare_schedule_json()
	
		

if __name__ == "__main__":
	main()
