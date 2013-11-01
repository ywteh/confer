import sys, os, operator, json

from py4j.java_gateway import JavaGateway
from py4j.java_collections import ListConverter


class Recommender:
	def __init__(self):
		self.gateway = JavaGateway()


	def get_item_based_recommendations(self, paper_id_list):
		java_paper_id_list = ListConverter().convert(
				paper_id_list, self.gateway._gateway_client)
		recs = self.gateway.entry_point.recommend(java_paper_id_list)
		res=[]
		for rec in recs:
			r = rec.split(',')
			res.append({'id': r[0], 'score': float(r[1])})

		return res

def main():
	r = Recommender()
	res = r.get_item_based_recommendations(['pn1460'])
	print res


if __name__ == "__main__":
	main()
