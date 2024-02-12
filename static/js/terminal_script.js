document.addEventListener('DOMContentLoaded', function () {
    const terminal = document.getElementById('terminal');
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    function createPrompt() {
        // Ensure there's no editable cmdInput before creating a new prompt
        const existingInput = terminal.querySelector('.cmdInput');
        if (existingInput) {
            existingInput.setAttribute('contenteditable', 'false'); // Disable editing for the previous input
        }

        const prompt = document.createElement('div');
        prompt.className = 'prompt';
        prompt.innerHTML = 'user@pc:~$ <span contenteditable="true" class="cmdInput"></span>';
        terminal.appendChild(prompt);
        focusOnInput();
    }

    function focusOnInput() {
        const cmdInput = terminal.querySelector('.cmdInput:last-of-type');
        cmdInput.focus();
        // Place cursor at end of contenteditable
        const range = document.createRange();
        const sel = window.getSelection();
        range.setStart(cmdInput, 1);
        range.collapse(true);
        sel.removeAllRanges();
        sel.addRange(range);
        autoScroll();
    }

    function autoScroll() {
        terminal.scrollTop = terminal.scrollHeight;
    }

    terminal.addEventListener('click', function() {
        focusOnInput();
    });

    terminal.addEventListener('keydown', function(e) {
        const cmdInput = document.querySelector('.cmdInput:last-of-type');
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const command = cmdInput.innerText.trim();
            if (command) {
                socket.emit('execute_command', { command: command });
                // Prevent further edits to the current input
                cmdInput.removeAttribute('contenteditable');
                cmdInput.parentElement.innerHTML = `user@pc:~$ ${command}`;
                // Append a placeholder for the output
                appendOutput('');
            }
        }
    });

    socket.on('command_output', function(msg) {
        // Correctly insert the output before the next prompt
        const outputs = terminal.querySelectorAll('.output');
        const lastOutput = outputs[outputs.length - 1];
        if (lastOutput) {
            lastOutput.textContent = msg; // Set the received message as output text
            createPrompt(); // Create a new prompt for the next command
        }
    });

    function appendOutput(msg) {
        const output = document.createElement('div');
        output.className = 'output';
        output.textContent = msg; // Initially empty or placeholder text
        terminal.appendChild(output);
    }

    createPrompt(); // Initialize the first prompt
});
