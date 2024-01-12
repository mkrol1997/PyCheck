function sendMessage() {
    let message_input = document.getElementById('message');
    let message = message_input.value;

    if (message) {
        socket.emit('send_message', {'channel': channel, 'message': message});
        message_input.value = "";
    }
}

function addMessageDiv(owner, message) {
    let msg_scroll_container = document.getElementById('messages-wrapper');
    let chat_messages_container = document.getElementById('chat-messages');
    let message_div = document.createElement('div');

    message_div.textContent = message;

    if ( message ) {
        message_div.classList.add('shadow');

        if ( owner == "sender") {
            message_div.classList.add('sender-message');

        } else {
            message_div.classList.add('receiver-message');
            message_div.classList.add('ml-auto');
        }
        chat_messages_container.appendChild(message_div);
        setTimeout(() => {
            msg_scroll_container.scrollTop = msg_scroll_container.scrollHeight;
        }, 0);

    }
}

document.getElementById('message_btn').addEventListener('click', sendMessage);
document.getElementById('message').addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        let message_input = document.getElementById('message');
        let message = message_input.value;

        sendMessage();
        addMessageDiv("sender", message);
    }
});

socket.on('handle_message', (message) => {
    addMessageDiv("receiver", message);
})
