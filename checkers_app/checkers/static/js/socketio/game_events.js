function getAvailableMoves() {
    return new Promise((resolve, reject) => {
        socket.emit("get_available_moves", {"channel": channel })

        socket.on('available_moves', (response) => {
            resolve(response.moves);
        });
    });
}

function getCordsAfterMove(pawn) {
     return new Promise((resolve, reject) => {
        let pawn_cords = pawn.getAttribute('data-position').split('-');
        socket.emit("get_cords_after_move",  {'pawn': pawn_cords, "channel": channel })

        socket.on('cords_after_move', (response) => {
            resolve(response.square_cords);
        });
    });
}

function movePawn(from_cords, to_cords) {
    socket.emit("make_move",  {'from_cords': from_cords, 'to_cords': to_cords, "channel": channel})
}

function updateBoard() {
    socket.emit('get_matrix', { "channel": channel });
    socket.on('receive_matrix', (data) => {
        drawChessBoard(data.matrix);
    });
}

function joinRoom() {
    socket.emit('join_room', { "room_id": channel});
}

function playGame(){
    getCurrentPlayerMoves();
}

socket.on('play_game', () => {
    playGame();
});

socket.on('handle_player_dc', () => {
    socket.emit('client_disconnect', { 'channel': channel });
});

socket.on("game_finished", (result) => {
    document.getElementById('result_reason').innerText = result.status;

    if (result.winner == '1') {
        document.getElementById('winner_img').src = pawn_black_img;
    } else {
        document.getElementById('winner_img').src = pawn_white_img;
    }
    $('#modalContent').modal('show');
});
