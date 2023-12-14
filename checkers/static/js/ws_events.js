var socket = io();

function main() {

    pawns_to_capture = [];
    findPawnsToCapture(currentPlayer)
        .then((response) => {
            console.log(response)
            pawns_to_capture = response;
            if (pawns_to_capture.length > 0) {
                response.forEach(pawnCoord => {
                    let dataCords = pawnCoord.join('-');
                    let elements = document.querySelectorAll(`[data-position="${dataCords}"]`);

                    highlightPossibleMoves(elements);
                    enablePawnsToCapture(elements);
                });
            } else {
                findPawnsToMove(currentPlayer)
                    .then((moves) => {
                        moves.pawns_cords.forEach(coord => {
                            let dataCords = coord.join('-');
                            let elements = document.querySelectorAll(`[data-position="${dataCords}"]`);

                            highlightPossibleMoves(elements);
                            enablePawnsToMove(elements);
                        });
                    })
                    .catch((moveError) => {
                        console.error("Error finding pawns to move:", moveError);
                    });
            }
        })
        .catch((captureError) => {
            console.error("Error finding pawns to capture:", captureError);
        });
}

function makeMove(from_square, to_square) {
    socket.emit('make_move', {from_cords: from_square, to_cords: to_square})
    currentPlayer = currentPlayer * -1;

    updateBoard();
    main();

}

function capturePawn(from_square, to_square) {
    socket.emit('make_capture', {from_cords: from_square, to_cords: to_square})
    currentPlayer = currentPlayer * -1;

    updateBoard();

    main();
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

function findPawnCaptures(square) {
        return new Promise((resolve, reject) => {
        let pawn_cords = getPawnCords(square);

        socket.emit("find_pawn_capture_cords", {'player': currentPlayer, 'pawn': pawn_cords});

        socket.on('found_pawn_captures', (data) => {
            let possible_moves = data;
            resolve(possible_moves);
        });
    });
}

function findPawnsToCapture(player) {
    return new Promise((resolve, reject) => {
        socket.emit('find_pawns_to_capture', { "player": player });

        socket.on('pawns_to_capture', (data) => {
            let pawns_to_capture = data.pawns_to_capture;
            resolve(pawns_to_capture);
        });
    });
}
