from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('terminal.html')

@socketio.on('execute_command')
def handle_execute_command(data):
    print('Received command from web:', data['command'])
    socketio.emit('execute_command', data)  # Relay command to client.py

@socketio.on('command_output')
def handle_command_output(data):
    print('Received output:', data['output'])
    socketio.emit('command_output', data['output'], include_self=False)  # Send output to web

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
