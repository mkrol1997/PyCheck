async function getCurrentPlayerMoves() {
    pawns_cords_with_legal_moves = await getAvailableMoves();

    if (pawns_cords_with_legal_moves.length > 0) {
        pawn_objects = queryPawnsUsingCords(pawns_cords_with_legal_moves);
        enablePawnsToBeSelected(pawn_objects);
        highlightPossibleMoves(pawn_objects);
    }
}

async function chooseSquareToMove(pawn, operation) {
    let move_to_cords_options = await getCordsAfterMove(pawn);
    let move_to_square_options = queryPawnsUsingCords(move_to_cords_options);

    move_to_square_options.forEach(square => {
        square.classList.add('move-to');
        square.addEventListener('click', (event) => {
            makeMove(pawn.getAttribute('data-position'), square.getAttribute('data-position'));
        });
    });
}

function makeMove(from_square, to_square) {
    movePawn(from_square, to_square)
    updateBoard()
}
