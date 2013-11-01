import sys, os, json, csv, re, difflib, operator
from collections import defaultdict
p = os.path.abspath(os.path.dirname(__file__) + '/../../data/cscw2014')
papers = {}

days = {}

abstracts = {}

prefs = defaultdict(set)

def get_s_id(s):
  return re.sub(r'\W+', '_', s)

def load_abstracts():
  f = open(p+'/cobi-authorsourcing.csv', 'rU')
  reader = csv.reader(f)
  for row in reader:
    if len(row) > 0:
      try:
        likes = row[11].lower().split(',')
        for like in likes:
          prefs[row[2].strip().lower()].add(like.strip())        
      except Exception, e:
        print e

  data = open(p+'/frenzy.json', 'rU').read()
  details = json.loads(data)
  f = open(p+'/cscw.csv', 'rU')
  reader = csv.reader(f)
  for row in reader:
    if len(row) > 0:
      try:
        d = details['items'][row[0]]['content']
        authors = row[10].strip().split(',')
        for author in authors:
          prefs[author.strip().lower()].add(row[0])
        papers[row[0]] = {'title': d['title'], 'authors': [{'name': name} for name in authors], 'abstract': d['fullAbstract']}
      except Exception, e:
        print e


def prepare_paper_and_schedule_json():
  load_abstracts()
  p = open('data/cscw2014/papers.json','w')
  p.write(json.dumps(papers))
  p = open('server/static/conf/cscw2014/data/papers.json','w')
  p.write('entities='+json.dumps(papers))
  for p in prefs:
    prefs[p] = list(prefs[p])
  p = open('data/cscw2014/prefs.json','w')
  p.write(json.dumps(prefs))
  print prefs
  


def main():
  prepare_paper_and_schedule_json()
       

if __name__ == "__main__":
        main()
