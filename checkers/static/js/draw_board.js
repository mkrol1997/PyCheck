function drawChessBoard(matrix) {
    const board = document.getElementById('chessBoard');
    board.innerHTML = '';
    let isWhite = true;

    for (let row = 0; row < matrix.length; row++) {
    for (let column = 0; column < matrix[row].length; column++) {

    const square = document.createElement('div');
    square.classList.add('square');

    if (isWhite) {
        square.classList.add('white');
    } else {
        square.classList.add('black');
    }

    const piece = matrix[row][column];

    if (piece === 1) {
        const pawn_black = document.createElement('img');
        pawn_black.src = pawn_black_img;
        pawn_black.alt = 'pawn_black';
        square.appendChild(pawn_black);

    } else if (piece === -1) {
        const pawn_white = document.createElement('img');
        pawn_white.src = pawn_white_img;
        pawn_white.alt = 'pawn_white';
        square.appendChild(pawn_white);
    }

    square.setAttribute("data-position", row + "-" + column)
    board.appendChild(square);
    isWhite = !isWhite;
}
    isWhite = !isWhite;
}
}
