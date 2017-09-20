from trie import *
import numpy as np
import textpreprocess
from collections import Counter
from time import time

tp = textpreprocess.Process('l')

class VectorSpaceModel:
	def __init__(self, trie, doc2idx):
		self.trie = trie
		self.doc2idx = doc2idx

	def get_relevant_docs(self, query, n=10):
		self.scores = np.zeros((len(self.doc2idx)/2,2))
		query_list = Counter(query)
		for word in query:
			try:
				query_eles = self.trie.check(word)
				query_idf = query_eles['idf']
				query_weight = query_list[word]*query_idf
				for key in query_eles.keys():
					if(key.strip() != '' and key.strip() != 'idf'):
						score = query_eles[key]*query_idf
						self.scores[self.doc2idx[key]][0] = self.doc2idx[key]
						self.scores[self.doc2idx[key]][1] += score
			except:
				pass
		self.top10 = self.scores[self.scores[:,1].argsort()[::-1]][:10]
		self.suggested_docs = [self.doc2idx[i[0]] for i in self.top10 if i[1] != 0]
		return self.suggested_docs


if __name__ == '__main__':
	trie = read_trie('trie/trie_l.pkl')
	doc2idx = read_trie('doc2idx/doc2idx.pkl')
	v = VectorSpaceModel(trie, doc2idx)
	start_time = time()
	print v.get_relevant_docs(['neural', 'network', 'nigga'])
	print(time()-start_time)