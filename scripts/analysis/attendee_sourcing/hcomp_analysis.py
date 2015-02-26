import sys, os, json, numpy, re
from collections import defaultdict
import matplotlib.pyplot as plt
p = os.path.abspath(os.path.dirname(__file__))


def prin_stats(d):
  print len(d), sum(d), max(d), min(d), numpy.mean(d), numpy.median(d), numpy.std(d)
 
def plot_hist(d1, title, y_label):
  plt.hist(d1, bins=1000, histtype='bar', color='yellow', label=y_label)
  #plt.title(title)
  #plt.ylabel(y_label)
  
  #plt.legend()
  plt.show()


def main():
  confer_data = json.loads(open(p+'/attendee-sourcing.json').read())

  confer_likes = {}
  for d in confer_data["data"]:
    if len(d["likes"]) > 0:
      confer_likes[d["id"]] = set(d["likes"])

  confer_likes_count = [len(confer_likes[k]) for k in confer_likes]

  confer_paper_likes = defaultdict(set)
  for id, likes in confer_likes.iteritems():
    for l in likes:
      confer_paper_likes[l].add(id)

  confer_paper_likes_count = [len(confer_paper_likes[k]) for k in confer_paper_likes]

  confer_affinity = defaultdict(dict)

  for p1 in confer_paper_likes:
    for p2 in confer_paper_likes:
      confer_affinity[p1][p2] = len(confer_paper_likes[p1].intersection(confer_paper_likes[p2]))
  
  confer_affinities = []
  cobi_affinities = []
  for p1 in confer_paper_likes:
    for p2 in confer_paper_likes:
      try:
        diff = confer_affinity[p1][p2] - cobi_affinity[p1][p2]
        if diff > 15 and cobi_affinity[p1][p2] == 0:
          print p1, p2
          confer_affinities.append(diff)
      except:
        pass


  prin_stats(confer_likes_count)
  prin_stats(cobi_likes_count)
  prin_stats(confer_paper_likes_count)
  prin_stats(cobi_paper_likes_count)

  #plot_hist(confer_affinities, 'Histogram of # of preferences', '# of preferences')


  


if __name__ == "__main__":
  main()
