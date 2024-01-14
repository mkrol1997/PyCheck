from __future__ import annotations

from checkers_app.game_engine.board import Board
from checkers_app.game_engine.game import Game


class Rooms:
    def __init__(self):
        self.current_games = {}

    @staticmethod
    def _create_new_game() -> Game:
        board = Board()
        game = Game(board)
        return game

    def add_new_game(self, channel: str) -> None:
        new_game = self._create_new_game()
        self.current_games[channel] = new_game

    def remove_game(self, channel: str) -> None:
        if channel in self.current_games:
            del self.current_games[channel]

    def get_channel_game(self, channel: str) -> Game:
        try:
            return self.current_games[channel]
        except KeyError:
            pass
