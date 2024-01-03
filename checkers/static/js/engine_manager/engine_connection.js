async function getCurrentPlayerMoves() {
    //  Highlights all pawns with legal moves

    pawns_cords_with_legal_moves = await getAvailableMoves();
    if (pawns_cords_with_legal_moves.length > 0) {

        pawn_objects = queryPawnsUsingCords(pawns_cords_with_legal_moves);
        enablePawnsToBeSelected(pawn_objects);
        highlightPossibleMoves(pawn_objects);

    } else {
        console.log("Game ended");
    }
}

async function chooseSquareToMove(pawn, operation) {
    //  Highlights and enables possible selected pawn moves

    let move_to_cords_options = await getCordsAfterMove(pawn);
    let move_to_square_options = queryPawnsUsingCords(move_to_cords_options);

    move_to_square_options.forEach(square => {
        square.style.backgroundColor = 'red';

        square.addEventListener('click', (event) => {
            makeMove(pawn.getAttribute('data-position'), square.getAttribute('data-position'));
        });
    });
}

function makeMove(from_square, to_square) {
    //  Moves pawn to selected square

    movePawn(from_square, to_square)

    updateBoard()
    getCurrentPlayerMoves()
}
