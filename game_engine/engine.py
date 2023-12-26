from __future__ import annotations

from typing import List, Tuple, Union

from constant import *
from game_engine.board import Board


class GameEngine:
    def __init__(self, board: Board):
        self.x = 0
        self.matrix = board.matrix
        self.cur_player = 1
        self.captures = {}
        self.basic_moves = {}

    def make_pawn_capture(self, capture_cords: tuple[int, int]) -> None:
        """Removes Pawn from the game board."""
        for capture in capture_cords:
            row, col = capture
            self.matrix[row][col].value = 0

    def move_pawn(self, from_cords: tuple[int, int], to_cords: tuple[int, int]) -> None:
        """Swaps positions between two squares."""
        from_row, from_col = from_cords
        to_row, to_col = to_cords

        if self.__should_pawn_become_king(move_to_row=to_row):
            self.matrix[from_row][from_col].is_king = True

        self.matrix[from_row][from_col], self.matrix[to_row][to_col] = (
            self.matrix[to_row][to_col],
            self.matrix[from_row][from_col],
        )

    def get_next_moves(self) -> Union[List[int, int], None]:
        """Returns list of possible next player moves coordinates."""
        if self.captures:
            return list(self.captures.keys())
        elif self.basic_moves:
            return list(self.basic_moves.keys())

    def switch_active_player(self) -> None:
        """Toggle player to perform next move."""
        self.cur_player *= -1

    def update_pawns_with_legal_moves(self) -> None:
        """Update list of pawns with either legal captures or basic moves."""
        self.captures = {}
        self.basic_moves = {}

        self.find_available_capture_moves()
        if not self.captures:
            self.find_available_basic_moves()

    def is_game_over(self) -> bool:
        """Checks if player still has moves available."""
        return not self.captures and not self.basic_moves

    def find_available_basic_moves(self) -> None:
        """Returns all possible basic moves with necessary coordinates."""

        player = self.cur_player

        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                pawn_cords = (row, column)
                check_dirs = [DIRECTIONS["forward_left"], DIRECTIONS["forward_right"]]

                if self.matrix[row][column].value != player:
                    continue

                if self.matrix[row][column].is_king:
                    check_dirs.extend([DIRECTIONS["back_left"], DIRECTIONS["back_right"]])

                for direction in check_dirs:
                    if self.__can_move_to_direction(*pawn_cords, direction=direction):
                        self.__add_move_coordinates(*pawn_cords, direction=direction)

    def find_available_capture_moves(self) -> None:
        """Returns all possible capture moves with necessary coordinates."""

        player = self.cur_player

        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                pawn_cords = (row, column)

                capture_dirs = [DIRECTIONS["forward_left"], DIRECTIONS["forward_right"]]

                if self.matrix[row][column].value != player:
                    continue

                if self.matrix[row][column].is_king:
                    capture_dirs.extend([DIRECTIONS["back_left"], DIRECTIONS["back_right"]])

                self.__get_capture_cords(pawn_cords, capture_dirs, pawn_cords, [], None)

    def __get_capture_cords(self, pawn_cords, directions, start, captures, last_move):
        row, column = pawn_cords
        found_captures = []

        for direction in directions:
            if self.__can_capture_at_direction(*pawn_cords, direction=direction):
                capture_cords = row - (direction[0] * self.cur_player), column - direction[1]
                move_to_cords = row - 2 * (direction[0] * self.cur_player), column - 2 * direction[1]
                found_captures.append((capture_cords, move_to_cords))

        if found_captures:
            for capture, move_to in found_captures:
                if capture not in captures:
                    self.__get_capture_cords(move_to, directions, start, captures + [capture], move_to)

        if captures:
            move_to = last_move
            self.__add_capture_coordinates(start, captures, move_to)

    def __should_pawn_become_king(self, move_to_row: int) -> bool:
        return move_to_row in (0, len(self.matrix) - 1)

    def __can_move_to_direction(self, row: int, column: int, direction: tuple[Union[-1, 1], Union[-1, 1]]) -> bool:
        """Checks if a pawn at given cords has available square to move towards given
        direction."""

        move_to_row, move_to_col = row - (direction[0] * self.cur_player), column - direction[1]

        if self.__has_valid_indexing(move_to_row, move_to_col):
            return False

        try:
            return self.matrix[move_to_row][move_to_col].value == 0
        except IndexError:
            return False

    def __add_move_coordinates(self, row: int, column: int, direction: tuple[Union[-1, 1], Union[-1, 1]]) -> None:
        """Adds square coordinates to the list of available basic pawn moves."""

        pawn_cords = (row, column)
        move_to_row, move_to_col = row - (direction[0] * self.cur_player), column - direction[1]

        try:
            pawn_basic_moves_cords = self.basic_moves[pawn_cords]

            if (move_to_row, move_to_col) not in pawn_basic_moves_cords:
                pawn_basic_moves_cords.append((move_to_row, move_to_col))
        except KeyError:
            self.basic_moves[pawn_cords] = [(move_to_row, move_to_col)]

    def __can_capture_at_direction(self, row: int, column: int, direction: tuple[Union[-1, 1], Union[-1, 1]]) -> bool:
        """Checks if a pawn at given cords has available opponent pawns to capture at his
        left side."""

        opponent_row, opponent_col = row - (direction[0] * self.cur_player), column - direction[1]
        move_to_row, move_to_col = row - 2 * (direction[0] * self.cur_player), column - 2 * direction[1]

        if self.__has_valid_indexing(opponent_row, opponent_col, move_to_row, move_to_col):
            return False

        return (
            self.matrix[opponent_row][opponent_col].value == self.cur_player * -1
            and self.matrix[move_to_row][move_to_col].value == 0
        )

    def __add_capture_coordinates(
        self, pawn_cords: Tuple[int, int], capture_cords: Tuple[int, int], move_to_cords: Tuple[int, int]
    ) -> None:
        """Adds square coordinates to the list of available basic pawn moves."""
        try:
            self.captures[pawn_cords][move_to_cords] = capture_cords

        except KeyError:
            self.captures[pawn_cords] = {move_to_cords: capture_cords}

    @staticmethod
    def __has_valid_indexing(*args: int) -> bool:
        """Disable array indexing with negative index; Applies to top and left board
        edges -> moves towards left and top border only."""
        return any(arg < 0 or arg > 7 for arg in args)
