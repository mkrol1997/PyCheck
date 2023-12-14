var socket = io();

function makeMove(from_square, to_square) {
    socket.emit('make_move', {from_cords: from_square, to_cords: to_square})
    currentPlayer = currentPlayer * -1;
    socket.emit('get_matrix');

    socket.on('receive_matrix', function(matrix) {
        drawChessBoard(matrix.matrix);
    });

    findPawnsToMove(currentPlayer)
        .then((moves) => {
            console.log(moves.pawns_cords);
            moves.pawns_cords.forEach(coord => {
                let data_cords = coord.join('-');
                let elements = document.querySelectorAll(`[data-position="${data_cords}"]`);

                highlightPossibleMoves(elements);
                enablePawnsToMove(elements);
            });
        })
        .catch((error) => {
            console.error(error);
        });
}

function findPawnsToMove(curr_player) {
    return new Promise((resolve, reject) => {
        socket.emit("find_pawns_to_move", {'current_player': curr_player });

        socket.on('found_legal_pawns', (data) => {
            let possible_moves = data;
            resolve(possible_moves);
        });
    });
}

function findPawnMoves(square) {
    return new Promise((resolve, reject) => {
        let pawn_cords = getPawnCords(square);

        socket.emit("find_pawn_moves", {
            'current_player': currentPlayer,
            'pawn': pawn_cords
        });

        socket.on('found_pawn_moves', (data) => {
            let possible_moves = data;
            resolve(possible_moves);
        });
    });
}
