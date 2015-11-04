import sys, json, csv, re, time

papers = {}
sessions = {}
schedule = []

dt_format='%m/%d/%Y'

def construct_id(s):
  return re.sub(r'\W+', '_', s)

def get_start_time(s_time):
  #return int(re.match(r'\d+', s_time).group())
  return s_time.split('-')[0].strip()

def get_date_time(s_date, dt_format='%m/%d/%Y'):
  if s_date == "Monday":
      return time.strptime('02/29/2016', dt_format)
  if s_date == 'Tuesday':
      return time.strptime('03/01/2016', dt_format)
  if s_date == 'Wednesday':
      return time.strptime('03/02/2016', dt_format)       
  #time_struct = time.strptime(s_date, dt_format)
  #return time_struct

def get_day(time_struct):
  return time.strftime("%A", time_struct)

def get_date(time_struct):
  return time.strftime("%m/%d/%Y", time_struct)

def get_class(s_time):
  v =  get_start_time(s_time)
  if(v < 10 and v >= 7):
    return 'morning1'
  elif(v >= 8 and v < 12):
    return 'morning2'
  elif(v >= 12 and v < 15):
    return 'afternoon1'
  elif(v >= 15 and v < 18):
    return 'afternoon2'
  else:
    return 'evening'

def prepare_schedule (t_schedule):
  # sort schedule data
  for s_date in t_schedule:
    t_schedule[s_date] = sorted(
      t_schedule[s_date].items(), key = lambda x: get_start_time(x[0]))

  print t_schedule
  t_schedule = sorted(t_schedule.items(), key=lambda x: time.mktime(get_date_time(x[0], dt_format=dt_format)))
  for day_schedule in t_schedule:
    slots = []
    s_date = day_schedule[0]
    all_slots = day_schedule[1]
    for slot_info in all_slots:
      slot_time = slot_info[0]
      slot_sessions = slot_info[1]['sessions']
      slots.append({
        'time': slot_time,
        'sessions': slot_sessions,
        'slot_class': get_class(slot_time),
        'slot_id': construct_id(s_date + slot_time)
      })
    schedule.append({'date': get_date(get_date_time(s_date, dt_format=dt_format)), 'slots': slots, 'day': get_day(get_date_time(s_date, dt_format=dt_format))})

def prepare_data(data_file1, data_file2):
  f1 = open(data_file1, 'rU')
  reader1 = csv.reader(f1)
  
  f2 = open(data_file2, 'rU')
  reader2 = csv.reader(f2)
  p_id = 1
  
  reader1.next()
  
  t_schedule = {}
  for row in reader1:
    paper_id = unicode(row[2], "ISO-8859-1")
    s_date = unicode(row[5], "ISO-8859-1").split(' ')[0]
    s_time = ' '.join(unicode(row[5], "ISO-8859-1").split(' ')[1:])
    #paper_type = unicode(row[2], "ISO-8859-1")
    session = unicode(row[0], "ISO-8859-1")
    room = unicode(row[1], "ISO-8859-1")
    paper_title = unicode(row[3], "ISO-8859-1")
    paper_authors = unicode(row[4], "ISO-8859-1")

    session = '%s-%s' % (session, room)
    # prepare papers data
    papers[paper_id] = {
        'title': paper_title,
        'subtype':'paper'}
    
    # prepare sessions data
    s_id = construct_id(session)
    if(s_id in sessions):
      sessions[s_id]['submissions'].append(paper_id)
    else:
      sessions[s_id] = {
          'submissions': [paper_id], 's_title': session, 'room': room, 'time': s_time, 'date': s_date}

    p_id += 1

  # prepare schedule data
  for session in sessions:
    s_info = sessions[session]
    s_date = s_info['date']
    s_time = s_info['time']
    s_data = {'session': session, 'room': s_info['room']}
    if s_date in t_schedule:
      if s_time in t_schedule[s_date]:
        t_schedule[s_date][s_time]['sessions'].append(s_data)
      else:
        t_schedule[s_date][s_time] = {'time': s_time, 'sessions':[s_data] }
    else:
      t_schedule[s_date] =  {s_time: {'time': s_time, 'sessions':[s_data]}}

  prepare_schedule(t_schedule)

  for i in range(4):
    reader2.next()
    
  for row in reader2:
    paper_id = unicode(row[0], "ISO-8859-1")[5:]
    paper_abstract = unicode(row[163], "ISO-8859-1")
    paper_authors = unicode(row[11], "ISO-8859-1")
    papers[paper_id]['abstract'] = paper_abstract
    papers[paper_id]['authors'] = [{'name': name.strip()} for name in paper_authors.strip('"').split(',')]

def main():
  conf = sys.argv[3]
  data_file1 = sys.argv[1]
  data_file2 = sys.argv[2]
  prepare_data(data_file1, data_file2)
  # write files
  p = open('data/' + conf + '/papers.json','w')
  p.write(json.dumps(papers, indent=2, sort_keys=True))
  p = open('server/static/conf/' + conf + '/data/papers.json','w')
  p.write('entities='+json.dumps(papers, indent=2, sort_keys=True))
  p = open('server/static/conf/' + conf + '/data/sessions.json','w')
  p.write('sessions='+json.dumps(sessions, indent=2, sort_keys=True))
  p = open('server/static/conf/' + conf +'/data/schedule.json','w')
  p.write('schedule='+json.dumps(schedule, indent=2, sort_keys=True))
  

if __name__ == "__main__":
  main()