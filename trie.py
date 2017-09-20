import textpreprocess
from collections import Counter
from time import time
import os
import numpy as np

class Trie:
	def __init__(self):
		self.children={}
		self.depth=0
		self.leaf_count=0

	def check(self, string, docname='', tf=0):
		#if character not a child, add a child node for that character
		if string[self.depth] not in self.children:
			self.children[string[self.depth]]=Node(string, self.depth, docname, tf)
		else:
			# if character is a child, traverse
			doc_dict=self.children[string[self.depth]].traverse(string, self.depth, docname, tf)
			return doc_dict

	def update_leaf_count(self, no_total_docs):
		if 'leafNode' in self.children.keys():
			self.leaf_count=1
			self.children['leafNode'].update_idf(no_total_docs)
		for child_idx in self.children.keys():
			if child_idx!='leafNode':
				self.children[child_idx].update_leaf_count(no_total_docs)
				self.leaf_count+=self.children[child_idx].leaf_count

	def query_suggestion(self,string):
			list_of_sugg = [] 
			orig_string = string
			top_suggestion = False;
			self.children[string[0]].suggest(string,list_of_sugg,top_suggestion)
			list_of_sugg.sort(key=lambda x: x[1])
			suggestions = []
			for ele in list_of_sugg:
				suggestions.append(ele[0])
			print suggestions
			return suggestions



class Node:
	def __init__(self, string, depth, docname, tf):
		self.depth=depth
		self.leaf_count=0
		self.children={}
		self.character=string[depth]

		# if not leaf node
		if len(string[self.depth+1:])>0: ############
			# check if child is present
			if string[self.depth+1] not in self.children.keys():
				self.add_node(string, docname, tf)
		else: # if leaf node
			self.add_leaf(string, docname, tf)
			#print('Adding leaf:', string)

	def add_node(self, string, docname, tf):
		self.children[string[self.depth+1]]=Node(string, self.depth+1, docname, tf)

	def add_leaf(self, string, docname, tf):
		self.children['leafNode']=Leaf(string, docname, tf) #add docid, tf

	def traverse(self, string, depth, docname, tf):
		if len(string[self.depth:])>1: #no leaf node to be added
			if string[self.depth+1] in self.children.keys():
				doc_dict=self.children[string[self.depth+1]].traverse(string, self.depth+1, docname, tf)
				return doc_dict
			else:
				self.add_node(string, docname, tf)	
		else: #add leaf
			if 'leafNode' in self.children.keys():
				#print('Leaf already exists:', string)
				self.children['leafNode'].add_doc(docname, tf)
				return self.children['leafNode'].docs
			else:
				#print('Creating leaf node:', string)
				self.add_leaf(string, docname, tf)
				return self.children['leafNode'].docs

	def update_leaf_count(self, no_total_docs): #call after making the entire trie. Pass total no of docs. It'll update the idf of each word.
		if 'leafNode' in self.children.keys():
			self.leaf_count=1
			self.children['leafNode'].update_idf(no_total_docs)
		for child_idx in self.children.keys():
			if child_idx!='leafNode':
				self.children[child_idx].update_leaf_count(no_total_docs)
				self.leaf_count+=self.children[child_idx].leaf_count
		#print(self.character, self.leaf_count)


	def suggest(self,string,list_of_sugg,top_suggestion):
		if self.leaf_count<=20:
			for i in self.children:
				if i=='leafNode':
					if top_suggestion ==True: 
						list_of_sugg.append([self.children['leafNode'].string,0])
					else:
						list_of_sugg.append([self.children['leafNode'].string,1])

				else:
					if len(string)>1:
						self.children[i].suggest(string[1:],list_of_sugg,top_suggestion)
					else:
						self.children[i].suggest(string[1:],list_of_sugg,top_suggestion)
						top_suggestion = True
		else:
			if(len(string)>1):
			 	y = string[1]
			 	next_substring = string[1:] 
			 	self.children[y].suggest(next_substring,list_of_sugg,top_suggestion)


class Leaf:
	def __init__(self,string, docname='INVALID', tf=0):
		self.string=string
		self.docs={docname:tf}
		self.df=len(self.docs)
		#self.df=len(self.docs)
		#self.tf=tf
		#self.df=len(self.docs)
		#print(self.docs)

	def add_doc(self,docname='INVALID', tf=0):
		self.docs[docname]=tf
		self.df=len(self.docs)
		#print(self.docs)

	def update_idf(self, no_total_docs):
		self.docs['idf']=np.log(no_total_docs/len(self.docs))

def save_trie(trie, filename):
	import pickle
	with open(filename, 'wb') as pFile:
	    pickle.dump(trie, pFile, -1) #HIGHEST_PROTOCOL
	return filename

def read_trie(filename):
	import pickle
	trie = None
	with open(filename, 'rb') as pFile:
	    trie = pickle.load(pFile)
	return trie

if __name__ == '__main__':
	pass
	# print('Trie saved to:', save_trie(tkn, 'not_trie.pkl'))
	# tr = read_trie('trie5.pkl')
