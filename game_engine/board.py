from game_engine.piece import Piece


class Board:
    def __init__(self):
        self.matrix = [
            [Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1)],
            [Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0)],
            [Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1)],
            [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
            [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
            [Piece(1), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0)],
            [Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(1)],
            [Piece(1), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0)],
        ]
