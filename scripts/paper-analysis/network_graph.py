
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
Finds all the cliques in the graph and prints various print_graph_stats
'''
def print_graph_stats(graph):
  cliques = [c for c in nx.find_cliques(graph)]

  num_cliques = len(cliques)

  clique_sizes = [len(c) for c in cliques]
  max_clique_size = max(clique_sizes)
  avg_clique_size = sum(clique_sizes) / num_cliques

  max_cliques = [c for c in cliques if len(c) == max_clique_size]

  num_max_cliques = len(max_cliques)

  max_clique_sets = [set(c) for c in max_cliques]
  nodes_in_all_max_cliques = list(
      reduce(lambda x, y: x.intersection(y), max_clique_sets))

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


'''
Constructs a network graph from an affinity_map

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


'''
Fetches data from the databse

For a given conf, returns a dictionary of <user: set(preferences)>

Sample Output:

{
  'rob': ('paper1', 'paper2', 'paper3'),
  'david': ('paper3', 'paper5', 'paper7')
}
'''
def get_user_preferences (conf):
  conference = Conference.objects.get(unique_name=conf)    
  users = Registration.objects.filter(conference=conference)

  user_preferences = defaultdict(set)
  for user in users:
    try: 
      preferences = json.loads(
          Likes.objects.get(registration=user).likes)

      user_preferences[user.id] = set(preferences)
    
    except Likes.DoesNotExist:
      pass

  return user_preferences


'''
For a given conference, generates 3 graphs

1) paper_person_graph: Each person and each paper is a node and there is an
                       edge between a paper and a person if the paper is in
                       the preference list of the person.

2) person_person_similarity_graph: Each person is a node and there is an edge
                                   between two people if they have one or more
                                   papers in common, with the weight = number
                                   of papers in common.

3) paper_paper_similarity_graph: Each paper is a node and there is an edge
                                 between two papers if one or more people have
                                 both the papers in their preference list, with
                                 the weight = number of people who have both
                                 the papers in their preference list.
'''
def get_network_graph (conf):
  user_preferences = get_user_preferences('cscw2015')
  paper_preferences = defaultdict(set)
  
  paper_person_graph = nx.Graph()
  for user, preferences in user_preferences.iteritems():    
    for paper in preferences:
      paper_person_graph.add_edge((user.id, 'person'), (paper, 'paper'))
      paper_preferences[paper].add(user.id)


  paper_paper_similarity_graph = construct_network_graph(paper_preferences)
  person_person_similarity_graph = construct_network_graph(user_preferences)

  return {
    'paper_person_graph': paper_person_graph,
    'paper_paper_similarity_graph': paper_paper_similarity_graph,
    'person_person_similarity_graph': person_person_similarity_graph
  }


def main():
  network = get_network_graph('cscw2015')
  person_person_similarity_graph = network['person_person_similarity_graph']
  print_graph_stats(person_person_similarity_graph)


if __name__ == "__main__":
  main()
