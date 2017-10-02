import textpreprocess
from collections import Counter
from time import time
import os
import numpy as np

class Trie:
	'''
	
	Class that implements the trie. It is directly linked to the root node.

	'''
	def __init__(self):
		'''
		Constructor for the class Trie. It'll initialize a new Trie.
		
		Examples
		--------
		>>> t=Trie()
		This will initialize a new Trie.
		'''
		self.children={}
		self.depth=0
		self.leaf_count=0

	def check(self, string, docname='', tf=0):
		'''
		Function that checks if a term is present in the trie. If present, the leaf node is updated
		with the new document and term-frequency. If not already present in the trie, a new leaf node
		is added to the trie.
		
		Parameters
		----------
		string : string
		    the string that is being checked for/inserted in the trie.
		docname : string, optional
			name of the document where the string comes from. default ''.
		tf : int, optional
		    the term frequency of the term in the particular document. default 0.

		Usage
		-----
		>>> t=Trie(string='car', docname='doc_1', tf=15)
		This means that the word 'car' was present in the document named 'doc_1', 15 times.
		This string, along with it's tf value, will be inserted into the trie.
        
		'''
		#if character not a child, add a child node for that character
		if string[self.depth] not in self.children:
			self.children[string[self.depth]]=Node(string, self.depth, docname, tf)
		else:
			# if character is a child, traverse
			doc_dict=self.children[string[self.depth]].traverse(string, self.depth, docname, tf)
			return doc_dict

	def update_leaf_count(self, no_total_docs):
		'''
		Function that updates the leaf_count of a node and all it's child nodes.
        Call this funcntion only after the entire trie has been built.
		
		Parameters
		----------
		no_total_docs : integer
			The trie that you wish to store to disk.

		Note
		-------
			Call this function only after bulding the entire trie.
		'''
		if 'leafNode' in self.children.keys():
			self.leaf_count=1
			self.children['leafNode'].update_idf(no_total_docs)
		for child_idx in self.children.keys():
			if child_idx!='leafNode':
				self.children[child_idx].update_leaf_count(no_total_docs)
				self.leaf_count+=self.children[child_idx].leaf_count

	def query_suggestion(self,string):
		'''
		Function that returns the top word suggestions.

		Returns
		----------
		list of strings
		Returns a list of the top suggestions.
		'''
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
	'''
	Class that implements a node in the trie.
	'''
	def __init__(self, string, depth, docname, tf):
		'''
		Constructor for the class Node. It'll initialize a new Node.

		Parameters
		----------
		string : string
		    the string that is being checked for/inserted in the trie.
		depth : string
		    the depth to which the string has been traversed.
		docname : string
			name of the document where the string comes from.
		tf : int, optional
		    the term frequency of the term in the particular document.
		'''
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
		'''
		Function to add a child node to the current node.

		Parameters
		----------
		string : string
		    the string that is being checked for/inserted in the trie.
		docname : string, optional
		    name of the document where the string comes from.
		tf : int, optional
		    the term frequency of the term in the particular document.
		'''
		self.children[string[self.depth+1]]=Node(string, self.depth+1, docname, tf)

	def add_leaf(self, string, docname, tf):
		'''
		Function that adds a leaf node as the child of the current node.

		Parameters
		----------
		string : string
		    the string that is being checked for/inserted in the trie.
		docname : string, optional
		    name of the document where the string comes from.
		tf : int, optional
		    the term frequency of the term in the particular document.
		'''
		self.children['leafNode']=Leaf(string, docname, tf) #add docid, tf

	def traverse(self, string, depth, docname, tf):
		'''
		Function to traverse the trie.

		Parameters
		----------
		string : string
		    the string that is being checked for/inserted in the trie.
		depth : string
		    the depth to which the string has been traversed.
		docname : string
			name of the document where the string comes from.
		tf : int, optional
		    the term frequency of the term in the particular document.
		'''
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
		'''
        Function that updates the leaf_count of a node and all it's child nodes.
        Call this funcntion only after the entire trie has been built.
		
		Parameters
		----------
		no_total_docs : integer
			The trie that you wish to store to disk.

		Note
		-------
			Call this function only after bulding the entire trie.
		'''
		if 'leafNode' in self.children.keys():
			self.leaf_count=1
			self.children['leafNode'].update_idf(no_total_docs)
		for child_idx in self.children.keys():
			if child_idx!='leafNode':
				self.children[child_idx].update_leaf_count(no_total_docs)
				self.leaf_count+=self.children[child_idx].leaf_count


	def suggest(self,string,list_of_sugg,top_suggestion):
		'''
		Function to get word suggestions.
		'''
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
	'''
	Class that implements a leaf node in the trie.
	'''
	def __init__(self,string, docname='INVALID', tf=0):
		'''
		Parameters
		----------
		string : string
		    the string that is being checked for/inserted in the trie.
		docname : string, optional
		    name of the document where the string comes from. By default 'INVALID'
		tf : int, optional
		    the term frequency of the term in the particular document. By default 0.
        '''
		self.string=string
		self.docs={docname:tf}
		self.df=len(self.docs)

	def add_doc(self,docname='INVALID', tf=0):
		'''
		Function to add a document to the current leaf.
		
		Parameters
		----------
		docname : string
			Name of the document to be added, default INVALID.
		filename : string
			The name of the file in which you wish to save the Trie.
		'''
		self.docs[docname]=tf
		self.df=len(self.docs)

	def update_idf(self, no_total_docs):
		'''
		Update idf of the current term. Adds a term with key- 'idf' to self.docs.

		Parameters
		----------
		no_total_docs : int
			Total number of documents in the corpus.
		'''
		self.docs['idf']=np.log(no_total_docs/len(self.docs))

def save_trie(trie, filename):
	'''
	Function to save a trie to disk.
	The Trie must be stored in pickled form, preferably using the function save_trie, 
	which is included in this file.

		Parameters
		----------
		trie : Trie object
			The trie that you wish to store to disk.
		filename : string
			The name of the file in which you wish to save the Trie.

		Returns
		-------
		string
			Returns the filename in which the trie has been saved.
	'''
	import pickle
	with open(filename, 'wb') as pFile:
	    pickle.dump(trie, pFile, -1) #HIGHEST_PROTOCOL
	return filename

def read_trie(filename):
	'''
	Function to read a trie from disk.
	The Trie must be stored in pickled form, preferably using the function save_trie, 
	which is included in this file.

	Parameters
	----------
	filename : string
	The name of the file in which you wish to save the Trie.

	Returns
	-------
	Trie object
	Returns the Trie that has been read from disk.
	'''
	import pickle
	trie = None
	with open(filename, 'rb') as pFile:
	    trie = pickle.load(pFile)
	return trie

if __name__ == '__main__':
	pass