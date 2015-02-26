
import json
import os
import networkx as nx
import sys
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt

if __name__ == "__main__":
  p = os.path.abspath(os.path.dirname(__file__))
  if(os.path.abspath(p+"/../..") not in sys.path):
    sys.path.append(os.path.abspath(p+"/../.."))
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from collections import defaultdict
from server.models import *

'''
Constructs a network graph from an affinity affinity_map

For Example:

Input

friends_affinity_map = {
  'rob': ['david', 'daniel', 'sam'],
  'david': ['rob', 'sam', 'anant'],
  'sam': ['rob', 'david', 'anant']
}

Output Graph:

Nodes = ['rob', 'anant', 'sam', 'david', 'daniel']
Edges = [
  {source: 'rob', target: 'david', 'weight': 1},
  {source: 'rob', target: 'sam', 'weight': 1},
  {source: 'david', target: 'sam', 'weight': 2}
]
'''

def construct_network_graph(affinity_map):
  network = nx.Graph()
  for key1 in affinity_map:
    for key2 in affinity_map:
      if key1 == key2:
        continue
      
      common_data = affinity_map[key1].intersection(affinity_map[key2])
      weight = len(common_data)
      
      if weight > 0:
        network.add_edge(
            key1, key2, weight=weight, common_data=list(common_data))

  return network


def get_network_graph (conf):
  paper_likes = defaultdict(set)
  person_likes = defaultdict(set)
  paper_person_graph = nx.Graph()
  conference = Conference.objects.get(unique_name=conf)    
  users = Registration.objects.filter(conference=conference)
  for user in users:
    try: 
      papers_liked_by_user = json.loads(
          Likes.objects.get(registration=user).likes)

      person_likes[user.id] = set(papers_liked_by_user)
      
      for paper in papers_liked_by_user:
        paper_person_graph.add_edge((user.id, 'person'), (paper, 'paper'))
        paper_likes[paper].add(user.id)
    
    except Likes.DoesNotExist:
      pass

  paper_paper_affinity_graph = construct_network_graph(paper_likes)
  person_person_affinity_graph = construct_network_graph(person_likes)

  return {
    'paper_person_graph': paper_person_graph,
    'paper_paper_affinity_graph': paper_paper_affinity_graph,
    'person_person_affinity_graph': person_person_affinity_graph
  }


def print_graph_stats(graph):
  cliques = [c for c in nx.find_cliques(graph)]

  num_cliques = len(cliques)

  clique_sizes = [len(c) for c in cliques]
  max_clique_size = max(clique_sizes)
  avg_clique_size = sum(clique_sizes) / num_cliques

  max_cliques = [c for c in cliques if len(c) == max_clique_size]

  num_max_cliques = len(max_cliques)

  max_clique_sets = [set(c) for c in max_cliques]
  nodes_in_all_max_cliques = list(reduce(lambda x, y: x.intersection(y),
                                    max_clique_sets))

  print 'Num cliques:', num_cliques
  print 'Avg clique size:', avg_clique_size
  print 'Max clique size:', max_clique_size
  print 'Num max cliques:', num_max_cliques
  print
  print 'nodes in all max cliques:'
  print json.dumps(nodes_in_all_max_cliques, indent=1)
  print
  print 'Max cliques:'
  print json.dumps(max_cliques, indent=1)


def main():
  network = get_network_graph('cscw2015')
  person_person_affinity_graph = network['person_person_affinity_graph']
  print_graph_stats(person_person_affinity_graph)


if __name__ == "__main__":
  main()
