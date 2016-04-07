import sys, json, csv, re, time



def prepare_papers(data_file):
  papers_dict = dict()
  f = open(data_file, 'rU')
  reader = csv.reader(f)  
  reader.next()

  for row in reader:
    paper_id = unicode(row[0], "ISO-8859-1")
    paper_title = unicode(row[1], "ISO-8859-1")
    paper_type = unicode(row[2], "ISO-8859-1").split(',', 1)[0].strip()
    abstract = unicode(row[3], "ISO-8859-1")
    paper_authors = unicode(row[4], "ISO-8859-1")   
    

    # prepare papers data
    papers_dict[paper_id] = {
        'id': paper_id,
        'title': paper_title,
        'subtype': paper_type,
        'type': paper_type,
        'abstract': abstract,
        'authors': [{'name': authors.split(',', 1)[0].strip()} for authors in paper_authors.split(';')]
    }

  return papers_dict


def main():
  conf = sys.argv[2]
  data_file = sys.argv[1]
  papers_dict = prepare_papers(data_file)
  # write files
  p = open('data/' + conf + '/papers.json','w')
  p.write(json.dumps(papers_dict, indent=2, sort_keys=True))
  p = open('server/static/conf/' + conf + '/data/papers.json','w')
  p.write('entities='+json.dumps(papers_dict, indent=2, sort_keys=True))
  #p = open('server/static/conf/' + conf + '/data/sessions.json','w')
  #p.write('sessions='+json.dumps(sessions, indent=2, sort_keys=True))
  #p = open('server/static/conf/' + conf +'/data/schedule.json','w')
  #p.write('schedule='+json.dumps(schedule, indent=2, sort_keys=True))
  

if __name__ == "__main__":
  main()
