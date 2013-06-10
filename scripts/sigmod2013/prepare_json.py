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
		p.write(json.dumps(papers))


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
				session_id = row[1]
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
	p.write(json.dumps(sessions))
	
		#print sessions


def main():
	prepare_paper_json()
	prepare_session_json()
	
		

if __name__ == "__main__":
	main()
