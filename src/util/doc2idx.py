import sys
sys.path.insert(0, '../')
import os
from trie import *

directory = os.path.join('../../data','abstract_')

filelist = os.listdir(directory)

if not os.path.exists('../doc2idx'):
    try:
        os.makedirs('../doc2idx')
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
            
file_to_idx={}
for file_idx, filename in enumerate(filelist):
	file_to_idx[file_idx]=filename[:-4]
	file_to_idx[filename[:-4]]=file_idx

print('file_to_idx saved to:',  save_trie(file_to_idx, '../doc2idx/doc2idx.pkl'))
