from flask import Flask
from flask_socketio import SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['ADDRESS'] = '172.16.47.29'
app.config['PORT'] = 8080
app.config['PATH'] = app.config['ADDRESS'] + ':' + str(app.config['PORT'])
app.config['trie'] = None
socketio = SocketIO(app, logger=False, engineio_logger=False, async_mode = 'gevent')
from app import views, sockets, api