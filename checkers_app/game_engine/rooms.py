from __future__ import annotations

from checkers_app.game_engine.board import Board
from checkers_app.game_engine.engine import GameEngine


class Rooms:
    def __init__(self):
        self.current_games = {}

    @staticmethod
    def _create_new_game() -> GameEngine:
        board = Board()
        game = GameEngine(board)
        return game

    def add_new_game(self, channel: str) -> None:
        new_game = self._create_new_game()
        self.current_games[channel] = new_game

    def remove_game(self, channel: str) -> None:
        if channel in self.current_games:
            del self.current_games[channel]

    def get_channel_game(self, channel: str) -> GameEngine:
        try:
            return self.current_games[channel]
        except KeyError:
            pass
