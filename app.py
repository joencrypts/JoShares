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

# Track users per channel
user_channels = { '1': set(), '2': set(), '3': set(), '4': set() }

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data.get('username', 'Anonymous')
    channel = str(data['channel'])
    join_room(channel)
    user_channels[channel].add(username)
    # Send current state to new user
    emit('sync', channels[channel], room=request.sid)
    # Notify others in the channel
    emit('system_message', {'message': f'👤 {username} joined the channel'}, room=channel)

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

@socketio.on('disconnect')
def on_disconnect():
    # Try to remove user from all channels and notify
    sid = request.sid
    for channel, users in user_channels.items():
        # This assumes username is unique per session; for production, use session IDs
        # For now, we can't get username from sid directly, so this is a limitation
        pass  # Frontend should emit a 'leave' event for accurate tracking

@socketio.on('leave')
def on_leave(data):
    username = data.get('username', 'Anonymous')
    channel = str(data['channel'])
    leave_room(channel)
    if username in user_channels[channel]:
        user_channels[channel].remove(username)
        emit('system_message', {'message': f'🚪 {username} left the channel'}, room=channel)

@socketio.on('chat_message')
def handle_chat_message(data):
    channel = str(data['channel'])
    username = data.get('username', 'Anonymous')
    message = data.get('message', '')
    reply_to = data.get('reply_to')  # Should be a dict: { 'username': ..., 'message': ... }
    emit('chat_message', {'username': username, 'message': message, 'reply_to': reply_to}, room=channel)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000) 