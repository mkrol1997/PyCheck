function queryPawnsUsingCords(list_of_cords){
    // Return pawn objects using their cords

    let found_pawns = [];

    list_of_cords.forEach(pawnCoord => {
        pawn_cords = pawnCoord.join('-')
        pawn_obj = document.querySelector(`[data-position="${pawn_cords}"]`);
        found_pawns.push(pawn_obj);
    });

    return found_pawns;
}


function highlightPossibleMoves(elements) {
    // Highlights all pawns able to perform valid capture/move

    elements.forEach(element => {
        element.style.backgroundColor = 'grey';
    })
};


function removePawnGreyBackground() {
    //  Sets default square background

    pawn_objects.forEach(pawn => {
        pawn.style.backgroundColor = '#b58863';
    });
}

function enablePawnsToBeSelected(pawns) {
    //  Enables pawns with legal moves to be selected

    pawns.forEach(pawn => {
        pawn.addEventListener('click', selectPawn)
    });
}

function disablePawnsToBeSelected(pawns) {
    //  Disables pawns with legal moves to be selected

    pawns.forEach(pawn => {
        pawn.removeEventListener('click', selectPawn)
    });
}

function selectPawn(event) {
    //  Shows available moves for selected pawn, disables the rest of them

    disablePawnsToBeSelected(pawn_objects);
    removePawnGreyBackground();
    chooseSquareToMove(event.currentTarget);
    event.target.style.backgroundColor = 'yellow';
}
