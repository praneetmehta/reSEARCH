import re
import os
import sys
import nltk
from nltk.stem import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

reload(sys)
sys.setdefaultencoding('utf8')

stemmer = PorterStemmer()
stop = set(stopwords.words('english'))
wordnet_lemmatizer = WordNetLemmatizer()

class Process:
	''' 
	
	This class is used for preprocessing text in files and queries, and tokenising 
	them after various preprocessing steps such as stemming and lemmetization
	
	'''
	
	def __init__(self, token_type='n'):
		self.type = token_type
	

	def processFile(self, text):
		'''
		returns the processed files

		It removes the special characters from the files, and certain expressions which were 
		converted from the scientific symbols. It then tokenises the file and then writes 
		the tokens into the file with length greater than 1 

		:param text: the text file to be processed
		:type text: text file
		:returns: file
		:rtype: text file
		'''
	
		text = re.sub('[#@&}~`:_;{]', '', text)
		text = file.replace('\\citet','').replace('\\textit','').replace('\n',' ')
		text = re.sub('\$(.*?)\$', '', text)
		text = re.sub('"','',text)
		text = re.sub('\\\\','',text)
		text = (' ').join([word for word in text.split(' ') if len(word)>1])
		text = re.sub(' +',' ',text)
		return text

	def processText(self, text):
		''' returns list of strings after preprocessing

			used for preprocessing words for insertion in the trie and query preprocessing.
			It converts all the characters to lower case, and uses stemming or lemetization according to need.
			It removes all the stop words and keeps only words whose length is greater than 2.

			:param text: files, query for preprocessing
	        :type text: text file, string
	        :returns: tokens
	        :rtype: list of strings
		'''
		text = re.sub('[^a-zA-Z]', ' ', text)
		tokens = nltk.word_tokenize(text)
		if self.type == 's':
			tokens = self.stem(tokens)
		elif self.type == 'l':
			tokens = self.lemmetize(tokens)
		else:
			pass
		tokens=[token.lower() for token in tokens if token.lower() not in stop]
		tokens = [token for token in tokens if len(token) > 2]
		return tokens
	
	def stem(self, tokens):
		''' returns tokens after stemming

			This function stems all the tokens using Porter Stemmer
		
			:param text: tokens
	        :type text: list of strings
	        :returns: stem_tokens
	        :rtype: list of strings
		'''
		stem_tokens = [stemmer.stem(token) for token in tokens]
		return stem_tokens

	def lemmetize(self, tokens):
		''' returns tokens after lemmatization

			This function lemmatizes all the tokens 

			:param text: tokens
	        :type text: list of strings
	        :returns: lemmatized
	        :rtype: list of strings
		'''
		lemmetized = [wordnet_lemmatizer.lemmatize(token) for token in tokens]
		return lemmetized

	def readAndProcessFiles(self, directory=os.path.join('../../data','abstract'), directory2=os.path.join('../../data','abstract_')):
		''' takes as input the directory from which the unprocessed files have to read and 
			the directory onto which the new processed files will be written back.
			If not specified, it takes the default values of input and output directories.
		'''
		if not os.path.exists(directory2):
		    try:
		        os.makedirs(directory2)
		    except OSError as exc: # Guard against race condition
		        if exc.errno != errno.EEXIST:
		            raise
		            
		filelist = os.listdir(directory)
		for f in enumerate(filelist):
			if(f[0]%1000 == 0):
				print(f[0])
			newtext = ''
			with open(os.path.join(directory, f[1]), 'r') as file:
				newtext = self.processFile(file.read())
			with open(os.path.join(directory2, f[1]), 'w+') as file:
				file.write(newtext)

if __name__ == "__main__":
	print('starting')