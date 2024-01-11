document.getElementById('message').addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        let message_input = document.getElementById('message');
        let message = message_input.value;

        if (message) {
            socket.emit('send_message', {'channel': channel, 'message': message});
            message_input.value = "";
        }
    }
});

document.getElementById('message_btn').addEventListener('click', (event) => {

    let message_input = document.getElementById('message');
    let message = message_input.value;

    if (message) {
        socket.emit('send_message', {'channel': channel, 'message': message});
        message_input.value = "";
    }

});

socket.on('handle_message', function(message) {
    let msg_scroll_container = document.getElementById('messages-wrapper');
    let chat_messages_container = document.getElementById('chat-messages');

    let message_div = document.createElement('div');

    message_div.textContent = message;
    message_div.classList.add('chat-message');
    message_div.classList.add('shadow');

    chat_messages_container.appendChild(message_div);

    setTimeout(() => {
        msg_scroll_container.scrollTop = msg_scroll_container.scrollHeight;
    }, 0);
})
