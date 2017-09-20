#!flask/bin/python
import sys
from app import app, socketio
from trie import *
import textpreprocess
import vector_space

try:
	token_type = raw_input('Enter token type(s/l/n): ')
	print('Loading Data...')
	app.config['processor'] = textpreprocess.Process(token_type)
	filename = 'trie/trie_'+token_type+'.pkl'
	app.config['trie'] = read_trie(filename)
	app.config['doc2idx'] = read_trie('doc2idx/doc2idx.pkl')
	app.config['vector'] = vector_space.VectorSpaceModel(app.config['trie'], app.config['doc2idx'])
	print 'loaded', filename
	print('Data Loaded. Server Starting...')
	socketio.run(app, debug=False,port=app.config['PORT'], host=app.config['ADDRESS'])
except KeyboardInterrupt:
	print('Now exiting')
	sys.exit()