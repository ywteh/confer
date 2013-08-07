import sys, os, json, csv, re, difflib
p = os.path.abspath(os.path.dirname(__file__) + '/../../data/kdd2013')

papers = {}
sessions = {}
schedule = []





def get_class(t):
	v =  int(t[0:2])
	if(v<10):
		return 'morning1'
	elif(v<12):
		return 'morning2'
	elif(v<15):
		return 'afternoon1'
	else:
		return 'afternoon2'


def load_files():
	data = open(p+'/papers.txt').read()
	rows = re.split(r'\n\n', data)
	for row in rows:
		try:
			details = re.split(r'\n', row)
			papers[details[0][10:]] = {'title':details[1][7:], 'authors':details[2][9:], 'abstract':''}
		except:
			pass
	data = open(p+'/sessions.txt').read()
	rows = re.split(r'\n\n', data)
	for row in rows:
		try:
			details = re.split(r'\n', row)
			sessions[details[0][9:]] = {'s_title':details[1][7:], 'submissions':[d[10:] for d in details[2:]]}
		except:
			pass
	

def prepare_paper_and_schedule_json():
	load_files()
	p = open('data/kdd2013/papers.json','w')
	p.write(json.dumps(papers))
	p = open('server/static/conf/kdd2013/data/papers.json','w')
	p.write('entities='+json.dumps(papers))
	p = open('server/static/conf/kdd2013/data/sessions.json','w')
	p.write('sessions='+json.dumps(sessions))
	p = open('server/static/conf/kdd2013/data/schedule.json','w')
	p.write('schedule='+json.dumps(schedule))


def main():
	prepare_paper_and_schedule_json()
       

if __name__ == "__main__":
        main()
