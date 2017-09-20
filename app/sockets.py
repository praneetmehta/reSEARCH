from app import socketio, app, api
from flask import render_template, request
import json
import requests
import threading
users = 0

@socketio.on('connection')
def handle_connection(data):
	global users
	users+=1
	print(json.loads(json.dumps(data))['data'])
	print('Total Users = '+str(users))

@socketio.on('disconnect')
def handle_disconnect():
	global users
	users-=1
	print('A User just disconnected')
	print('Total Users = '+str(users))

@socketio.on('typing')
def handle_typing(query):
	user_sid = request.sid
	res = json.loads(json.dumps(query))['data']
	t = threading.Thread(target=get_res, args=(res, user_sid))
	t.start()
	
@socketio.on('query_submit')
def search_for_query(data):
	user_sid = request.sid
	query = json.loads(json.dumps(data))['data']
	t = threading.Thread(target=fetch_docs, args=(query, user_sid))
	t.start()

def get_res(res, user_sid):
	response = requests.get('http://'+app.config['PATH']+'/api/auto_complete?partial_query='+res).text
	socketio.emit('update_suggestions', json.loads(response),broadcast=False, room=user_sid)
	socketio.sleep(0)
	return 0

def fetch_docs(query, user_sid):
	response = requests.get('http://'+app.config['PATH']+'/api/fetch_docs?query='+query).text
	socketio.emit('update_results', json.loads(response), broadcast = False, room=user_sid)
	return 0