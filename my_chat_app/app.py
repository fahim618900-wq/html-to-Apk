import os
import json
import base64
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HISTORY_FILE = "chat_history.json"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)

users = {}  # sid -> username

# Chat history load করা
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        chat_history = json.load(f)
else:
    chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat_history')
def get_history():
    return jsonify(chat_history)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

def add_message(msg):
    chat_history.append(msg)
    save_history()

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username
    msg = {"type":"system","text": f"{username} joined the chat!"}
    add_message(msg)
    emit('message', msg, broadcast=True)

@socketio.on('message')
def handle_message(text):
    username = users.get(request.sid, "Unknown")
    msg = {"type":"chat","user":username,"text":text}
    add_message(msg)
    emit('message', msg, broadcast=True)

@socketio.on('file')
def handle_file(data):
    filename = secure_filename(data['filename'])
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(data['filedata']))

    username = users.get(request.sid, "Unknown")
    msg = {"type":"file","user":username,"filename":filename,"url": f"/uploads/{filename}"}
    add_message(msg)
    emit('message', msg, broadcast=True)

@socketio.on('delete')
def handle_delete(index):
    # Safety check
    if 0 <= index < len(chat_history):
        chat_history.pop(index)
        save_history()
        emit('delete', index, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = users.get(request.sid, "Someone")
    msg = {"type":"system","text": f"{username} left the chat."}
    add_message(msg)
    emit('message', msg, broadcast=True)
    users.pop(request.sid, None)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=6189, debug=True, use_reloader=False)