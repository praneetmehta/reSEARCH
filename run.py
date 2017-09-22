#!flask/bin/python
import sys
from app import app, socketio
from trie import *
import textpreprocess
import vector_space

# try starting the server
try:
	#type of data to load (s = stemmed, l = lemmetized, n = no_preprocessing)
	try:	#handle input for different python versions
		token_type = raw_input('Enter token type(s/l/n): ')
	except:
		token_type = input('Enter token type(s/l/n): ')

	print('Loading Data...')
	filename = 'trie/trie_'+token_type+'.pkl'

	#load global module objects textpreprocessor, trie, doc2idx and vector score calculator
	app.config['processor'] = textpreprocess.Process(token_type)
	app.config['trie'] = read_trie(filename)
	app.config['doc2idx'] = read_trie('doc2idx/doc2idx.pkl')
	app.config['vector'] = vector_space.VectorSpaceModel(app.config['trie'], app.config['doc2idx'])

	print('Data Loaded. Server Starting...')
	
	#establish socket.io stream and run server
	socketio.run(app, debug=False,port=app.config['PORT'], host=app.config['ADDRESS'])
	print('Server running at' + str(app.config['PATH']))
	
except KeyboardInterrupt:
	print('Now exiting')
	sys.exit()