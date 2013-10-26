import sys, os, json, re, datetime

from db.entity import *
from db.session import *

p = os.path.abspath(os.path.dirname(__file__))

days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']

def get_class(t):
  v =  int(re.match(r'\d+', t).group())
  if(v < 10 and v >= 8):
    return 'morning1'
  if(v < 12 and v >= 10):
    return 'morning2'
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


def main():
  e = Entity()
  s = Session()
  f = open(p + '/../../data/chi2013/papers.json','w')
  f.write(json.dumps(e.entities))
  schedule = {}
  final_schedule = []
  sessions = s.get_sessions()

  for s in sessions:
    dt = sessions[s]['day']
    tm = sessions[s]['time']
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

  sorted_s = sorted(schedule.items(), key=lambda x: days.index(x[0].lower()))
  for dt in sorted_s:
    slots = []
    for tm in dt[1]:
      k = tm[1]
      slots.append({
        'time': k['time'],
        'sessions': k['sessions'],
        'slot_class': get_class(k['time']),
        'slot_id': get_id(dt[0], k['time'])
        })

    final_schedule.append({'date': dt[0], 'slots': slots, 'day': dt[0]})
  print final_schedule
  f = open(p +'/../../data/chi2013/sessions.json','w')
  f.write(json.dumps(sessions))
  f = open(p +'/../../data/chi2013/schedule.json','w')
  f.write(json.dumps(final_schedule))
  print "done"


if __name__ == "__main__":
	main()
