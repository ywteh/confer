import sys, os, json, csv, re, difflib
p = os.path.abspath(os.path.dirname(__file__) + '/../../data/ijcai2013')

papers = {}
sessions = {}
schedule = []


def load_abstracts():
	f = open(p+'/abstracts.csv', 'rU')
	reader = csv.reader(f)
	for row in reader:
		papers[row[0]] = {
			'title': unicode(row[1], "ISO-8859-1"),
			'abstract': unicode(row[2], "ISO-8859-1")}



def handle_session(session):
	if('papers' not in session.keys()):
		return
	sessions['session_'+session['sessionid']] = {
		's_title': session['title'],
		'submissions': [p['paperid'] for p in session['papers']]
	}
	for p in session['papers']:
		paper_id = p['paperid']
		if(paper_id in papers):
			authors = re.split(',', p['authors'])

			papers[paper_id].update(
				{'authors':[{'name': author} for author in authors]})
		else:
			#print session
			pass


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



def handle_file(f, date, day):
	data = json.loads(open(p+'/'+f).read())
	day = {'date': date, 'day': day}
	s_slots = []
	for slot_id, slot in data.iteritems():
		if 'sessions' not in slot.keys():
			continue
		s_slot = {'time':slot['nom_slot'], 'slot_id': 'slot_'+slot_id, 'slot_class': get_class(slot['nom_slot'])}
		sessions = []
		for session_id, session in slot['sessions'].iteritems():
			sessions.append({'session': 'session_'+session['sessionid'], 'room': session['room']})
			handle_session(session)
		s_slot['sessions'] = sessions
		s_slots.append(s_slot)
	day['slots'] = s_slots
	schedule.append(day)

def prepare_paper_and_schedule_json():
	load_abstracts()
	handle_file('6.json', '08/06/2013', 'Tuesday')
	handle_file('7.json', '08/07/2013', 'Wednesday')
	handle_file('8.json', '08/08/2013', 'Thursday')
	handle_file('9.json', '08/09/2013', 'Friday')
	p = open('data/ijcai2013/papers.json','w')
	p.write(json.dumps(papers))
	p = open('server/static/conf/ijcai2013/data/papers.json','w')
	p.write('entities='+json.dumps(papers))
	p = open('server/static/conf/ijcai2013/data/sessions.json','w')
	p.write('sessions='+json.dumps(sessions))
	p = open('server/static/conf/ijcai2013/data/schedule.json','w')
	p.write('schedule='+json.dumps(schedule))


def main():
	prepare_paper_and_schedule_json()
       

if __name__ == "__main__":
        main()
