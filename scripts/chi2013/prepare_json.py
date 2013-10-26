import sys, os, json

from db.entity import *
from db.session import *

p = os.path.abspath(os.path.dirname(__file__))

def main():
	e = Entity()
	s = Session()
	f = open(p + '/../../data/chi2013/papers.json','w')
	f.write(json.dumps(e.entities))
	f = open(p +'/../../data/chi2013/sessions.json','w')
	f.write(json.dumps(s.sessions))
	print "done"


if __name__ == "__main__":
	main()
