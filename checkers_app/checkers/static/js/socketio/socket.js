var socket = io();

socket.on("connect", () => {
    socket.emit('user_connected', { "channel": channel });
});
