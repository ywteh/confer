
import json
import os
import networkx as nx
import sys
from networkx.readwrite import json_graph

if __name__ == "__main__":
  p = os.path.abspath(os.path.dirname(__file__))
  if(os.path.abspath(p+"/../..") not in sys.path):
    sys.path.append(os.path.abspath(p+"/../.."))
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from collections import defaultdict
from server.models import *

def get_network_graph (conf):
  paper_likes = defaultdict(set)
  people_likes = defaultdict(set)
  paper_person_graph = nx.Graph()
  paper_paper_graph = nx.Graph()
  
  try:
    conference = Conference.objects.get(unique_name=conf)    
    users = Registration.objects.filter(conference=conference)
    for user in users:
      try: 
        papers_liked_by_user = json.loads(
            Likes.objects.get(registration=user).likes)

        people_likes[user.id] = set(papers_liked_by_user)
        
        for paper in papers_liked_by_user:
          paper_person_graph.add_edge((user.id, 'person'), (paper, 'paper'))
          paper_likes[paper].add(user.id)
      
      except Likes.DoesNotExist:
        pass

    for paper1 in paper_likes:
      for paper2 in paper_likes:
        if paper1 == paper2:
          continue
        
        weight = len(paper_likes[paper1].intersection(paper_likes[paper2]))
        if weight > 0:
          paper_paper_graph.add_edge(paper1, paper2, weight=weight)

    return {
      'paper_paper_graph': paper_paper_graph,
      'paper_person_graph': paper_person_graph
    }
  except Exception, e:
    print e

def main():
  network = get_network_graph('cscw2015')
  json.dump(
      json_graph.node_link_data(network['paper_person_graph']),
      open('data.json','w'))


if __name__ == "__main__":
  main()
