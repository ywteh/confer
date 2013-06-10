import sys, os, json, csv

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/../..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/../.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")





def main():
	f = open('data/sigmod2013/prog_ck.csv','r')
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
				paper_id = unicode(row[1], "ISO-8859-1")
				session = unicode(row[0], "ISO-8859-1")
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
		print papers

if __name__ == "__main__":
	main()
