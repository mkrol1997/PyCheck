from __future__ import annotations

from typing import List, Tuple, Union

from checkers_app.game_engine.game import Game
from constant import *


class GameEngine:
    def move_pawn(self, game: Game, from_cords: Tuple[int, int], to_cords: Tuple[int, int]) -> None:
        from_row, from_col = from_cords
        to_row, to_col = to_cords

        if self._should_pawn_become_king(board=game.board, move_to_row=to_row):
            game.board.matrix[from_row][from_col].is_king = True

        game.board.matrix[from_row][from_col], game.board.matrix[to_row][to_col] = (
            game.board.matrix[to_row][to_col],
            game.board.matrix[from_row][from_col],
        )

    def find_available_basic_moves(self, game: Game) -> None:
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                pawn_cords = (row, column)
                check_dirs = [DIRECTIONS["forward_left"], DIRECTIONS["forward_right"]]

                if game.board.matrix[row][column].value != game.active_player:
                    continue

                if game.board.matrix[row][column].is_king:
                    check_dirs.extend([DIRECTIONS["back_left"], DIRECTIONS["back_right"]])

                for direction in check_dirs:
                    if self._can_move_to_direction(game, *pawn_cords, direction=direction):
                        self._add_move_coordinates(game, *pawn_cords, direction=direction)

    def find_available_capture_moves(self, game: Game) -> None:
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):

                pawn_cords = (row, column)
                capture_dirs = [DIRECTIONS["forward_left"], DIRECTIONS["forward_right"]]

                if game.board.matrix[row][column].value != game.active_player:
                    continue

                if game.board.matrix[row][column].is_king:
                    capture_dirs.extend([DIRECTIONS["back_left"], DIRECTIONS["back_right"]])

                self._get_capture_cords(game, pawn_cords, capture_dirs, pawn_cords, [], None)

    def _get_capture_cords(
        self,
        game: Game,
        pawn_cords: Tuple[int, int],
        directions: List[Tuple[int, int]],
        start: Tuple[int, int],
        captures: List[Tuple[int, int]],
        last_move: Union[Tuple[int, int], None],
    ):
        row, column = pawn_cords
        found_captures = []
        for direction in directions:
            if self._can_capture_at_direction(game, *pawn_cords, direction=direction):
                capture_cords = row - (direction[0] * game.active_player), column - direction[1]
                move_to_cords = row - 2 * (direction[0] * game.active_player), column - 2 * direction[1]
                found_captures.append((capture_cords, move_to_cords))

        if found_captures:
            for capture, move_to in found_captures:
                if capture not in captures:
                    self._get_capture_cords(game, move_to, directions, start, captures + [capture], move_to)

        if captures:
            move_to = last_move
            self._add_capture_coordinates(game, start, captures, move_to)

    @staticmethod
    def get_next_moves(game) -> Union[List[int, int], None]:
        if game.captures:
            return list(game.captures.keys())
        elif game.basic_moves:
            return list(game.basic_moves.keys())

    @staticmethod
    def make_pawn_capture(game: Game, capture_cords: Tuple[int, int]) -> None:
        for capture in capture_cords:
            row, col = capture
            game.board.matrix[row][col].value = 0

    @staticmethod
    def switch_active_player(game) -> None:
        game.active_player *= -1

    def update_pawns_with_legal_moves(self, game: Game) -> None:
        game.captures = {}
        game.basic_moves = {}

        self.find_available_capture_moves(game)
        if not game.captures:
            self.find_available_basic_moves(game)

    @staticmethod
    def is_game_over(game) -> bool:
        return not game.captures and not game.basic_moves

    @staticmethod
    def _should_pawn_become_king(board: Game, move_to_row: int) -> bool:
        return move_to_row in (0, len(board.matrix) - 1)

    def _can_move_to_direction(
        self, game: Game, row: int, column: int, direction: Tuple[Union[-1, 1], Union[-1, 1]]
    ) -> bool:
        move_to_row, move_to_col = row - (direction[0] * game.active_player), column - direction[1]

        if self.__has_valid_indexing(move_to_row, move_to_col):
            return False

        try:
            return game.board.matrix[move_to_row][move_to_col].value == 0
        except IndexError:
            return False

    @staticmethod
    def _add_move_coordinates(game, row: int, column: int, direction: Tuple[Union[-1, 1], Union[-1, 1]]) -> None:
        pawn_cords = (row, column)
        move_to_row, move_to_col = row - (direction[0] * game.active_player), column - direction[1]

        try:
            pawn_basic_moves_cords = game.basic_moves[pawn_cords]

            if (move_to_row, move_to_col) not in pawn_basic_moves_cords:
                pawn_basic_moves_cords.append((move_to_row, move_to_col))
        except KeyError:
            game.basic_moves[pawn_cords] = [(move_to_row, move_to_col)]

    def _can_capture_at_direction(
        self, game: Game, row: int, column: int, direction: Tuple[Union[-1, 1], Union[-1, 1]]
    ) -> bool:
        opponent_row, opponent_col = row - (direction[0] * game.active_player), column - direction[1]
        move_to_row, move_to_col = row - 2 * (direction[0] * game.active_player), column - 2 * direction[1]

        if self.__has_valid_indexing(opponent_row, opponent_col, move_to_row, move_to_col):
            return False

        return (
            game.board.matrix[opponent_row][opponent_col].value == game.active_player * -1
            and game.board.matrix[move_to_row][move_to_col].value == 0
        )

    @staticmethod
    def _add_capture_coordinates(
        game, pawn_cords: Tuple[int, int], capture_cords: Tuple[int, int], move_to_cords: Tuple[int, int]
    ) -> None:

        try:
            game.captures[pawn_cords][move_to_cords] = capture_cords
        except KeyError:
            game.captures[pawn_cords] = {move_to_cords: capture_cords}

    @staticmethod
    def __has_valid_indexing(*args: int) -> bool:
        return any(arg < 0 or arg > 7 for arg in args)
