var socket = io();

socket.on("connect", () => {
    console.log("USER CONNECTED TO CHANNEL: " + channel)
    socket.emit('user_connected', { "channel": channel });
});
