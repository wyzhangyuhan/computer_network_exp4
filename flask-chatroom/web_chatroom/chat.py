from flask import Blueprint
from flask import render_template,flash,redirect,url_for
from flask import request
from flask_login import current_user, login_required
from web_chatroom import models
from web_chatroom import db
from werkzeug.utils import secure_filename
import os

chat = Blueprint('chat', __name__)


@chat.route('/chat', methods=['GET', "POST"],endpoint='chat')
@login_required
def chatroom():
    if request.method == 'GET':
        message_list = db.session.query(models.Message).order_by(models.Message.id).all()
        message_list.reverse()
        message_list = message_list[:9]
        message_list.reverse()
        return render_template('chatroom.html',message_list=message_list)

@chat.route('/upload', methods=['POST'])
@login_required
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        print("-----")
        print(f.filename)
        print("-----")
        upload_path = os.path.join(basepath, f.filename)
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html')