function queryPawnsUsingCords(list_of_cords){
    let found_pawns = [];

    list_of_cords.forEach(pawnCoord => {
        pawn_cords = pawnCoord.join('-')
        pawn_obj = document.querySelector(`[data-position="${pawn_cords}"]`);
        found_pawns.push(pawn_obj);
    });
    return found_pawns;
}

function highlightPossibleMoves(elements) {
    elements.forEach(element => {
        element.classList.add('selection');
    })
};

function removePawnGreyBackground() {
    pawn_objects.forEach(pawn => {
        pawn.classList.remove('selection');
    });
}

function enablePawnsToBeSelected(pawns) {
    pawns.forEach(pawn => {
        pawn.addEventListener('click', selectPawn)
    });
}

function disablePawnsToBeSelected(pawns) {
    pawns.forEach(pawn => {
        pawn.removeEventListener('click', selectPawn)
    });
}

function selectPawn(event) {
    disablePawnsToBeSelected(pawn_objects);
    removePawnGreyBackground();
    chooseSquareToMove(event.currentTarget);
    highlightSelectedPawn(event.target);
}

function highlightSelectedPawn(pawn) {
    if (pawn.tagName == 'IMG') {
        pawn.parentNode.classList.add('selected');
    } else {
        pawn.classList.add('selected');
    }
}

function showModal() {
    $('#modalContent').modal('show');
}

function copyToClipboard(text) {
    console.log("Copy to CLIPBOARD not available using HTTP");
}
