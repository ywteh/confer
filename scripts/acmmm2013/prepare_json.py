import sys, os, json, csv, re, difflib, operator
p = os.path.abspath(os.path.dirname(__file__) + '/../../data/acmmm2013')
print p
papers = {}
sessions = {}
schedule = {}
final_schedule = []


days = {}

abstracts = {}

paper_type = ['papers', 'keynote', 'doctorial symposium', 'demos', 'posters', 'grand challenge', 'brave new topics', 'open source']

def load_abstracts():
	f = open(p+'/confer-mainprog-acmmm13.tsv', 'rU').read()
	rows = f.split('\n')
	for row in rows:
		row = unicode(row, "ISO-8859-1")
		data = row.split('\t')
		if data[11] in paper_type:
			papers[data[0]] = {'title': data[1], 'authors': [{'name': name} for name in data[2].strip('"').split(',')], 'abstract': data[3]}
			if(data[5] in sessions):
				sessions[data[5]]['submissions'].append(data[0])
			else:
				sessions[data[5]] = {'submissions': [data[0]], 's_title': data[5], 'date': data[7],'start':int(re.match(r'\d+', data[8]).group()), 'time': data[8] + '-' + data[9], 'room': data[10]}
	
	for s in sessions:
		sessions[s]['submissions'] = list(set(sessions[s]['submissions']))



def get_class(t):
	v =  int(re.match(r'\d+', t).group())
	if(v < 12 and v >= 8):
		return 'morning'
	elif(v>= 12 and v<15):
		return 'afternoon1'
	elif(v>=15 and v<18):
		return 'afternoon2'
	else:
		return 'evening'

def get_id(d, t):
	v =  re.sub(':', '_', t)
	v =  re.sub('-', '_', v)
	return d + '_' + v

def get_day(d):
	if(d == '10/23/13'):
		return 'Wednesday'
	elif(d == '10/24/13'):
		return 'Thursday'
	elif(d == '10/25/13'):
		return 'Friday'

def load_files():
	load_abstracts()
	for s in sessions:
		dt = sessions[s]['date']
		tm = sessions[s]['start']
		if dt in schedule:
			if tm in schedule[dt]:
				schedule[dt][tm]['sessions'].append({'session': s, 'room': sessions[s]['room']})
			else:
				schedule[dt][tm] = {'time': sessions[s]['time'],
				'sessions':[{'session': s, 'room': sessions[s]['room']}]
				}
		else:
			schedule[dt] =  {tm: 
				{'time': sessions[s]['time'],
				'sessions':[{'session': s, 'room': sessions[s]['room']}]
				}
			}

	for s in schedule:
		schedule[s] = sorted(schedule[s].items(), key=lambda x: x[0])

	sorted_s = sorted(schedule.items(), key=lambda x: x)
	for dt in sorted_s:
		slots = []
		for tm in dt[1]:
			k = tm[1]
			slots.append({
				'time': k['time'],
				'sessions': k['sessions'],
				'slot_class': get_class(k['time']),
				'slot_id': get_id(get_day(dt[0]), k['time'])
				})

		final_schedule.append({'date': dt[0], 'slots': slots, 'day': get_day(dt[0])})
	print final_schedule


def prepare_paper_and_schedule_json():
	load_abstracts()
	load_files()
	#print papers
	p = open('data/acmmm2013/papers.json','w')
	p.write(json.dumps(papers))
	p = open('server/static/conf/acmmm2013/data/papers.json','w')
	p.write('entities='+json.dumps(papers))
	p = open('server/static/conf/acmmm2013/data/sessions.json','w')
	p.write('sessions='+json.dumps(sessions))
	p = open('server/static/conf/acmmm2013/data/schedule.json','w')
	p.write('schedule='+json.dumps(final_schedule))
	


def main():
	prepare_paper_and_schedule_json()
       

if __name__ == "__main__":
        main()
