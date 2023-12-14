from __future__ import annotations

from checkers.checkers_game import Board


class Validator:
    def __init__(self, board):
        self.matrix = board

    def find_pawns_available_to_move(self, current_player):
        legal_moves = Validator._find_pawns_to_capture(self, player=current_player)

        if legal_moves:
            return legal_moves

        def is_valid_move(row, column):
            return 0 <= row < 8 and 0 <= column < 8

        for row in range(8):
            for column in range(8):
                if self.matrix[row][column] == current_player:
                    if (
                        is_valid_move(row - 1 * current_player, column + 1)
                        and self.matrix[row - 1 * current_player][column + 1] == 0
                    ):
                        legal_moves.append((row, column))
                    if (
                        is_valid_move(row - 1 * current_player, column - 1)
                        and self.matrix[row - 1 * current_player][column - 1] == 0
                    ):
                        legal_moves.append((row, column))

        return list(set(legal_moves))

    def find_pawn_legal_moves(self, player, pawn_cords):
        pawn_cords = [int(cord) for cord in pawn_cords]

        legal_moves = self._get_capture_cords(pawn_cords, player)

        if not legal_moves:
            try:
                if self.matrix[pawn_cords[0] - 1 * player][pawn_cords[1] - 1] == 0:
                    legal_moves.append([pawn_cords[0] - 1 * player, pawn_cords[1] - 1])
            except IndexError:
                pass

            try:
                if self.matrix[pawn_cords[0] - 1 * player][pawn_cords[1] + 1] == 0:
                    legal_moves.append([pawn_cords[0] - 1 * player, pawn_cords[1] + 1])
            except IndexError:
                pass

        return legal_moves

    def _find_pawns_to_capture(self, player):
        legal_moves = []

        if player == 1:
            for row in range(8):
                for column in range(8):
                    try:
                        if (
                            self.matrix[row][column] == player
                            and self.matrix[row - 1][column + 1] == -1
                            and self.matrix[row - 2][column + 2] == 0
                        ):
                            legal_moves.append((row, column))
                    except IndexError:
                        pass
                    try:
                        if (
                            self.matrix[row][column] == player
                            and self.matrix[row - 1][column - 1] == -1
                            and self.matrix[row - 2][column - 2] == 0
                        ):
                            legal_moves.append((row, column))
                    except IndexError:
                        pass
        else:
            for row in range(8):
                for column in range(8):
                    try:
                        if (
                            self.matrix[row][column] == player
                            and self.matrix[row + 1][column + 1] == 1
                            and self.matrix[row + 2][column + 2] == 0
                        ):
                            legal_moves.append((row, column))

                    except IndexError:
                        pass
                    try:
                        if (
                            self.matrix[row][column] == player
                            and self.matrix[row + 1][column - 1] == 1
                            and self.matrix[row + 2][column - 2] == 0
                        ):
                            legal_moves.append((row, column))
                    except IndexError:
                        pass

        return legal_moves

    def _get_capture_cords(self, pawn_cords, player):
        legal_moves = []

        try:
            if (
                self.matrix[pawn_cords[0] - 1 * player][pawn_cords[1] - 1] == player * -1
                and self.matrix[pawn_cords[0] - 2 * player][pawn_cords[1] - 2] == 0
            ):
                legal_moves.append([pawn_cords[0] - 2 * player, pawn_cords[1] - 2])
        except IndexError:
            pass

        try:
            if (
                self.matrix[pawn_cords[0] - 1 * player][pawn_cords[1] + 1] == player * -1
                and self.matrix[pawn_cords[0] - 2 * player][pawn_cords[1] + 2] == 0
            ):
                legal_moves.append([pawn_cords[0] - 2 * player, pawn_cords[1] + 2])
        except IndexError:
            pass

        return legal_moves
