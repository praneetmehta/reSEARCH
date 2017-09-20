import sys
sys.path.insert(0, '../')
import os
from trie import *

directory = os.path.join('../Unstructured_','abstract_')

filelist = os.listdir(directory)

file_to_idx={}
for file_idx, filename in enumerate(filelist):
	file_to_idx[file_idx]=filename[:-4]
	file_to_idx[filename[:-4]]=file_idx

print('file_to_idx saved to:',  save_trie(file_to_idx, '../doc2idx/doc2idx.pkl'))
