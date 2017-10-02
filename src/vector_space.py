from trie import *
import numpy as np
import textpreprocess
from collections import Counter
from time import time

tp = textpreprocess.Process('l')

class Evaluate:
	'''

	Class to evaluate scores based on tf-idf weights and determine similarity
	between documents and the query to return as well as determining keywords 
	relevant to each document.

	Initializer takes in two inputs, a data-structure, 'trie', and a doc2idx dictionary, 
	containing mappings of document names to unique integer values.

	>>> e = Evaluate()

	'''
	def __init__(self, trie, doc2idx):
		'''
		Initializer for the Evaluate class.
		
		Parameters
		----------
		trie - Data structure to query words and fetch idf scores
		doc2idx - Dictionary containing mapping between document names and unique identifiers(integers)
		'''
		self.trie = trie
		self.doc2idx = doc2idx

	def get_relevant_docs(self, query, n=10):
		'''
		fetch the relevant n documents by calculating cosine similarity between the documents
		and the search query.

		Parameters
		----------
		query = list of query terms (tokenized and preprocessed returned from the server)
		n = total number of documents to be returned.

		Return
		------
		n relevant documents with the top similarity score
		'''
		self.scores = np.zeros((len(self.doc2idx)/2,2))
		query_list = Counter(query)
		for word in query:
			try:
				query_eles = self.trie.check(word)
				query_idf = query_eles['idf']
				query_weight = query_list[word]*query_idf
				for key in query_eles.keys():
					if(key.strip() != '' and key.strip() != 'idf'):
						score = query_eles[key]*query_idf*query_weight
						self.scores[self.doc2idx[key]][0] = self.doc2idx[key]
						self.scores[self.doc2idx[key]][1] += score
			except:
				pass
		self.top10 = self.scores[self.scores[:,1].argsort()[::-1]][:10]
		self.suggested_docs = [i for i in self.top10 if i[1] != 0]
		print self.suggested_docs
		return self.suggested_docs

	def fetch_keywords(self, doc_text, threshold=10):
		'''
		Fetch keywords from the document, i.e. the words withing the document with the highest
		tf-idf score. Higher score means these words better describe this document.

		Parameters
		----------
		doc_text = list of tokenized text from the document
		threshold = minimum score for the word(token) for it to be considered a keyword.

		Return
		------
		Dictionary with keys as the keywords and values as the scores.
		'''
		tokens = tp.processText(doc_text)
		keys = Counter(tokens)
		self.pair = []
		for key in keys:
			imp = keys[key]*self.trie.check(key)['idf']
			self.pair.append([key, int(imp)])
		self.pair = sorted(self.pair,key=lambda l:l[1], reverse=True)
		return self.pair[:5]

if __name__ == '__main__':
	trie = read_trie('trie/trie_l.pkl')
	doc2idx = read_trie('doc2idx/doc2idx.pkl')
	e = Evaluate(trie, doc2idx)
	start_time = time()
	print(e.get_relevant_docs(['neural', 'network', 'nigga']))
	print(time()-start_time)