import sys
from app import app
from flask import request
import json
from trie import *
from time import time

@app.route('/api/auto_complete')
def api_autoComplete():
	''' REST-api end point for getting n word suggestions
	based on the partial query typed by the user'''
	partial_query = request.args.get('partial_query')
	if(partial_query.isspace() or partial_query==''):
		suggestions = []
	else:
		suggestions = app.config['trie'].query_suggestion(partial_query)
	data = []
	for word in suggestions:
		temp = {'suggestion':word}
		data.append(temp)
	response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
	return response

@app.route('/api/fetch_docs')
def api_fetchDocs():
	''' Fetch relevant n documents matching the user submitted query
	based on the cosine similarity between the documents and the search 
	query '''
	query = request.args.get('query')
	processed_text = app.config['processor'].processText(query)
	print(processed_text)
	time_results = {'retrieval':'','render':''}
	start_time = time()
	rel_docs = app.config['vector'].get_relevant_docs(processed_text)
	time_results['retrieval'] = 'Retrieved '+str(len(rel_docs))+' documents in:  ',str(time()-start_time) + ' seconds'
	# print rel_docs
	# docs = t.fetch_docs(processed_text)
	start_time = time()
	results = []
	root = 'Unstructured_/'
	for doc in rel_docs:
		doc = app.config['doc2idx'][doc[0]]
		temp = {
			'title':'Title',
			'authors':'Authors',
			'subject':'Subject',
			'link':'link',
			'doc_text':'This is the content for the 1st document',
			'keywords':[{'key':'Keyword1'}, {'key':'Keyword2'},{'key':'Keyword3'}]
		}
		with open(root+'abstract_/'+doc+'.txt', 'r') as file:
			temp['doc_text'] = file.read()
			keywords = app.config['vector'].fetch_keywords(temp['doc_text'])
			temp['keywords'] = []
			for keyword in keywords:
				temp['keywords'].append({'key':keyword[0].title()})
		with open(root+'title/'+doc+'.txt','r') as file:
			temp['title'] = file.read()
		with open(root+'authors/'+doc+'.txt','r') as file:
			temp['authors'] = file.read()
		with open(root+'subject/'+doc+'.txt','r') as file:
			temp['subject'] = file.read()
		with open(root+'link/'+doc+'.txt','r') as file:
			temp['link'] = file.read()
		results.append(temp)
	time_results['render'] = 'File reading and rendering Time:  ',str(time()-start_time) + ' seconds'
	results.append(time_results)
	response = app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )
	return response