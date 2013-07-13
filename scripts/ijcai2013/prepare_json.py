import sys, os, json, csv, re, difflib

if __name__ == "__main__":
        p = os.path.abspath(os.path.dirname(__file__))
        if(os.path.abspath(p+"/../..") not in sys.path):
                sys.path.append(os.path.abspath(p+"/../.."))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

papers = {}
sessions = {}

def prepare_paper_and_schedule_json():
	try:
		file = open('6', 'rU')
		f = json.loads(file.read())
		for key in f.keys():
                  if ('sessions' in f[key]):
                    item = f[key]['sessions']
		    for session in item:
                      session_id = item[session]['sessionid']
		      s_title = item[session]['title']
		      submissions = []
                      if 'papers' in item[session]:
                	for paper in item[session]['papers']:
       			  authors = []
                          paper_id = paper['paperid']
   			  author_list = re.split(",",  paper['authors'])
			  for author in author_list:
			     authors.append({'name': author})
			  print authors
			  title = paper['paper']
			  session = f[key]['nom_slot']
			  abstract = ""
			  papers[paper_id] = {'authors': authors, 'title': title, 'abstract':abstract, 'session': session}
			  #print papers[paper_id]
			  submissions.append(paper_id)
		      sessions[session_id]={'s_title': s_title, 'submissions':submissions}
	except:
		print sys.exc_info()


def main():
        prepare_paper_and_schedule_json()
        p = open('../../server/static/json/ijcai2013/papers.json','w')
        p.write('entities='+json.dumps(papers))
	p = open('../../data/ijcai2013/papers.json','w')
        p.write(json.dumps(papers))

        p = open('../../server/static/json/ijcai2013/sessions.json','w')
	p.write('sessions='+json.dumps(sessions))


if __name__ == "__main__":
        main()
