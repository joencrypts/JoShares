from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
import eventlet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Store playback state per channel
channels = {
    '1': {},
    '2': {},
    '3': {},
    '4': {},
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data.get('username', 'Anonymous')
    channel = str(data['channel'])
    join_room(channel)
    # Send current state to new user
    emit('sync', channels[channel], room=request.sid)
    emit('user_joined', {'username': username}, room=channel)

@socketio.on('play')
def on_play(data):
    channel = str(data['channel'])
    state = {
        'video_id': data['video_id'],
        'timestamp': data['timestamp'],
        'is_playing': True
    }
    channels[channel] = state
    emit('play', state, room=channel, include_self=False)

@socketio.on('pause')
def on_pause(data):
    channel = str(data['channel'])
    channels[channel]['is_playing'] = False
    channels[channel]['timestamp'] = data['timestamp']
    emit('pause', {'timestamp': data['timestamp']}, room=channel, include_self=False)

@socketio.on('seek')
def on_seek(data):
    channel = str(data['channel'])
    channels[channel]['timestamp'] = data['timestamp']
    emit('seek', {'timestamp': data['timestamp']}, room=channel, include_self=False)

@socketio.on('change_video')
def on_change_video(data):
    channel = str(data['channel'])
    state = {
        'video_id': data['video_id'],
        'timestamp': 0,
        'is_playing': False
    }
    channels[channel] = state
    emit('change_video', state, room=channel)

@socketio.on('chat_message')
def handle_chat_message(data):
    channel = str(data['channel'])
    username = data.get('username', 'Anonymous')
    message = data.get('message', '')
    emit('chat_message', {'username': username, 'message': message}, room=channel)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000) 