function movePiece(square) {
    square.style.backgroundColor = 'green';
    findPawnMoves(square)
        .then((moves) => {
            moves.pawns_cords.forEach(coord => {
                let data_cords = coord.join('-');
                let elements = document.querySelectorAll(`[data-position="${data_cords}"]`);
                elements.forEach(element => {
                    element.style.backgroundColor = 'yellow';
                    element.addEventListener('click', (event) => {
                        makeMove(square.getAttribute('data-position'), element.getAttribute('data-position'));
                    });
                })
            });
        })
        .catch((error) => {
            console.error(error);
        });
}

function capturePiece(square) {
    square.style.backgroundColor = 'green';
    findPawnCaptures(square)
        .then((moves) => {
            moves.capture_cords.forEach(coord => {
                    let data_cords = coord.join('-');
                    let elements = document.querySelectorAll(`[data-position="${data_cords}"]`);
                    elements.forEach(element => {
                        element.style.backgroundColor = 'yellow';
                        element.addEventListener('click', (event) => {
                            capturePawn(square.getAttribute('data-position'), element.getAttribute('data-position'));
                        });
                    })
                });
            })
    .catch((error) => {
        console.error(error);
    });
}

function findPawnsToMove(board_state, curr_player) {
    return new Promise((resolve, reject) => {
        socket.emit("find_pawns_to_move", {'board_state': board_state, 'current_player': curr_player });

        socket.on('found_legal_pawns', (data) => {
            let possible_moves = data;
            resolve(possible_moves);
        });
    });
}


function highlightPossibleMoves(elements) {
    elements.forEach(element => {
        element.style.backgroundColor = 'grey';
    })
};

function enablePawnsToMove(pawns) {
    pawns.forEach(pawn => {
        pawn.addEventListener('click', (event) => {
        movePiece(event.currentTarget);
    });
});
}


function getPawnCords(square) {
    return square.getAttribute('data-position').split('-');
}

function enablePawnsToCapture(pawns) {
    pawns.forEach(pawn => {
        pawn.addEventListener('click', (event) => {
            capturePiece(event.currentTarget);
        });
    });
}

function updateBoard() {
    socket.emit('get_matrix');

    socket.on('receive_matrix', function(matrix) {
        drawChessBoard(matrix.matrix);
    });
}

function main() {
    updateBoard();

    findPawnsToCapture(currentPlayer)
        .then((response) => {
            pawns_to_capture = response;
            if (pawns_to_capture.length > 0) {
                console.log("CAPTURE")
                response.forEach(pawnCoord => {
                    let dataCords = pawnCoord.join('-');
                    let elements = document.querySelectorAll(`[data-position="${dataCords}"]`);

                    highlightPossibleMoves(elements);
                    enablePawnsToCapture(elements);
                });
            } else {
                console.log("MOVE")
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
