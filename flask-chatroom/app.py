'''
Author: your name
Date: 2021-04-11 10:53:25
LastEditTime: 2021-04-14 09:15:03
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \web_chatroom\app.py
'''
from web_chatroom import create_app,db
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_socketio import SocketIO

import eventlet
app = create_app()

socketio = SocketIO(app, async_mode='eventlet')
from web_chatroom.request_hook import *

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

from web_chatroom.socketioutils import *



if __name__ == '__main__':
    # manager.run()
    socketio.run(app,host='0.0.0.0')
    # socketio.run(app, host="127.0.0.1")
