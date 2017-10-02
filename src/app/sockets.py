from app import socketio, app, api
from flask import render_template, request
import json
import requests
import threading
users = 0

'''user connection event '''
@socketio.on('connection')
def handle_connection(data):
	''' Handle user connection event and
		update the user count '''
	global users
	users+=1
	print(json.loads(json.dumps(data))['data'])
	print('Total Users = '+str(users))

''' User disconnect event '''
@socketio.on('disconnect')
def handle_disconnect():
	''' Handle the user disconnect event and
		update the user count '''
	global users
	users-=1
	print('A User just disconnected')
	print('Total Users = '+str(users))

''' Handle typing event -> When the user types in 
	the search query field'''
@socketio.on('typing')
def handle_typing(query):
	''' Handle typing event emitted by the client
		and provide provide suggestions '''
	user_sid = request.sid
	res = json.loads(json.dumps(query))['data']
	t = threading.Thread(target=get_res, args=(res, user_sid))
	t.start()
	
''' User query_submit event '''
@socketio.on('query_submit')
def search_for_query(data):
	''' Handle query submit and document retrieval calls'''
	user_sid = request.sid
	query = json.loads(json.dumps(data))['data']
	t = threading.Thread(target=fetch_docs, args=(query, user_sid))
	t.start()

def get_res(res, user_sid):
	''' Hit the REST endpoint for word suggestion and fetch 
		and emit update_suggestions event '''
	response = requests.get('http://'+app.config['PATH']+'/api/auto_complete?partial_query='+res).text
	socketio.emit('update_suggestions', json.loads(response),broadcast=False, room=user_sid)
	socketio.sleep(0)
	return 0

def fetch_docs(query, user_sid):
	''' HIT the REST endpoint for document retrieval and 
		emit the update_results event '''
	response = requests.get('http://'+app.config['PATH']+'/api/fetch_docs?query='+query).text
	socketio.emit('update_results', json.loads(response), broadcast = False, room=user_sid)
	return 0