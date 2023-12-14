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
};


function getPawnCords(square) {
    return square.getAttribute('data-position').split('-');
}
