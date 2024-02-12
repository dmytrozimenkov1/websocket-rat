document.addEventListener('DOMContentLoaded', function () {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('command_output', function(msg) {
        const outputElement = document.getElementById('output');
        outputElement.textContent += '\n' + msg;
        outputElement.scrollTop = outputElement.scrollHeight; // Scroll to bottom
    });

    document.getElementById('sendCommand').addEventListener('click', function() {
        const command = document.getElementById('commandInput').value;
        socket.emit('execute_command', { command: command });
        document.getElementById('commandInput').value = ''; // Clear input field
    });
});
