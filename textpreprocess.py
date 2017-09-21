import re
import os
import sys
import nltk
from nltk.stem import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
reload(sys)
sys.setdefaultencoding('utf8')

stemmer = PorterStemmer()
stop=set(stopwords.words('english'))

class Process:
	def __init__(self, token_type='n'):
		self.type = token_type

	def processFile(self, text):
		text = re.sub('[#@&}~`:_;{]', '', text)
		text = file.replace('\\citet','').replace('\\textit','').replace('\n',' ')
		text = re.sub('\$(.*?)\$', '', text)
		text = re.sub('"','',text)
		text = re.sub('\\\\','',text)
		text = (' ').join([word for word in text.split(' ') if len(word)>1])
		text = re.sub(' +',' ',text)
		return text

	def processText(self, text):
		# file = (' ').join([word.lower() for word in text.split(' ') if len(word)>1])
		# text = re.sub('[#@&}~`:_;{"]', '', text)
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
		stem_tokens = [stemmer.stem(token) for token in tokens]
		return stem_tokens

	def lemmetize(self, tokens):
		lemmetized = [wordnet_lemmatizer.lemmatize(token) for token in tokens]
		return lemmetized

	def readAndProcessFiles(self, directory=os.path.join('../Unstructured_','abstract'), directory2=os.path.join('../Unstructured_','abstract_')):
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
