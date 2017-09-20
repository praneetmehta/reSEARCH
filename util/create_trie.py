from __future__ import division
import sys
sys.path.insert(0, '../')
from trie import *
from time import time
import numpy as np
import textpreprocess
try:
	processor = textpreprocess.Process(sys.argv[1])
	filename = 'trie_'+sys.argv[1]+'.pkl'
except:
	processor = textpreprocess.Process('')
	print('none type selected')
	filename = 'trie_n.pkl'
tr = Trie()
directory = os.path.join('../Unstructured_','abstract_')

filelist = os.listdir(directory)

if not os.path.exists('../trie'):
    try:
        os.makedirs('../trie')
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

start_time=time()
# tkn = []
for f in enumerate(filelist):
	if(f[0]%10 == 0):
		print(f[0])
	with open(os.path.join(directory, f[1]), 'r') as file:
		tokens = processor.processText(file.read())
		# tkn+=tokens
		normalization_factor = len(tokens)
		temp=Counter(tokens)
		# normalization_factor = 0
		# for word in temp.keys():
		# 	normalization_factor+=temp[word]**2
		# normalization_factor = np.sqrt(normalization_factor)
		for word in temp.keys():
			tr.check(word, f[1][:-4], temp[word]/normalization_factor)
tr.update_leaf_count(len(filelist))
print('Trie saved to:', save_trie(tr, '../trie/'+filename))
print('Trie created in:', time()-start_time)