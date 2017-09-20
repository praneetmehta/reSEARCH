from flask import render_template
from app import socketio, app
import json

@app.route('/')
def index():
	return render_template('index.html', title="Search Engine")

