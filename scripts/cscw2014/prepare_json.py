import sys, os, json, csv, re, difflib, operator
p = os.path.abspath(os.path.dirname(__file__) + '/../../data/cscw2014')
papers = {}




days = {}

abstracts = {}

paper_type = ['papers', 'keynote', 'doctorial symposium', 'demos', 'posters', 'grand challenge', 'brave new topics', 'open source']

def get_s_id(s):
	return re.sub(r'\W+', '_', s)

def load_abstracts():
	data = open(p+'/frenzy.json', 'rU').read()
	details = json.loads(data)
	f = open(p+'/cscw.csv', 'rU')
	reader = csv.reader(f)
	for row in reader:
		if len(row) > 0:
			try:
				d = details['items'][row[0]]['content']
				papers[row[0]] = {'title': d['title'], 'authors': [{'name': name} for name in row[10].strip('"').split(',')], 'abstract': d['fullAbstract']}
			except Exception, e:
				print e
	



def prepare_paper_and_schedule_json():
	load_abstracts()
	p = open('data/cscw2014/papers.json','w')
	p.write(json.dumps(papers))
	p = open('server/static/conf/acmmm2013/data/papers.json','w')
	p.write('entities='+json.dumps(papers))
	


def main():
	prepare_paper_and_schedule_json()
       

if __name__ == "__main__":
        main()
