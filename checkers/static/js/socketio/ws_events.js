function getAvailableMoves() {
    // Returns cords of all legal pawns to move

    return new Promise((resolve, reject) => {
        socket.emit("get_available_moves")

        socket.on('available_moves', (response) => {
            resolve(response.moves);
        });
    });
}

function getCordsAfterMove(pawn) {
    // Returns coordinates of all possible squares to move the selected pawn to

     return new Promise((resolve, reject) => {
        let pawn_cords = pawn.getAttribute('data-position').split('-');
        socket.emit("get_cords_after_move",  {'pawn': pawn_cords})

        socket.on('cords_after_move', (response) => {
            resolve(response.square_cords);
        });
    });
}

function movePawn(from_cords, to_cords) {
    // Performs pawn move

    socket.emit("make_move",  {'from_cords': from_cords, 'to_cords': to_cords})
}

function updateBoard() {
    // Draws current board matrix representation

    socket.emit('get_matrix');

    socket.on('receive_matrix', function(matrix) {
        drawChessBoard(matrix.matrix);
    });
}
