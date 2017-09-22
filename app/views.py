from flask import render_template
from app import socketio, app
import json

@app.route('/')
def index():
	''' Render the home page '''
	return render_template('index.html', title="Search Engine")

