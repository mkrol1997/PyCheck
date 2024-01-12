from checkers_app.game_engine.board import Board


class Game:
    def __init__(self, board: Board):
        self.board = board
        self.active_player = 1
        self.captures = {}
        self.basic_moves = {}
