import pytest

from checkers_app.game_engine.board import Board
from checkers_app.game_engine.engine import GameEngine
from checkers_app.game_engine.piece import Piece
from constant import DIRECTIONS


@pytest.fixture
def game_engine():
    board = Board()
    engine = GameEngine(board)
    return engine


def test_should_return_true_when_all_white_pawns_capture_moves_added_to_captures(game_engine):
    game_engine.cur_player = 1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {(4, 3): {(2, 1): [(3, 2)]}}

    assert expected == result


def test_should_return_true_when_no_captures_are_available_for_white_pawn_at_the_board_edges(game_engine):
    game_engine.cur_player = 1
    game_engine.matrix = [
        [Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0)],
        [Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(1)],
        [Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1)],
        [Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
        [Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1)],
        [Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
        [Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1)],
        [Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
    ]

    game_engine.find_available_capture_moves()
    result = game_engine.captures
    expected = {}

    assert expected == result


def test_should_return_true_when_white_king_pawn_can_not_capture_across_vertical_edges(game_engine):
    game_engine.cur_player = 1
    game_engine.matrix = [
        [Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1)],
    ]

    game_engine.matrix[1][2].is_king = True
    game_engine.matrix[6][6].is_king = True
    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {}

    assert expected == result


def test_should_return_true_when_all_white_pawn_captures_added_to_dictionary(game_engine):
    game_engine.cur_player = 1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0)],
        [Piece(0), Piece(1), Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0)],
    ]

    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {
        (3, 2): {(1, 4): [(2, 3)]},
        (4, 6): {(2, 4): [(3, 5)]},
        (6, 1): {(4, 3): [(5, 2)]},
        (6, 6): {(2, 6): [(5, 5), (3, 5)], (4, 4): [(5, 5)]},
    }

    assert expected == result


def test_should_return_true_when_white_pawn_multiple_captures_are_available(game_engine):
    game_engine.cur_player = 1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {
        (7, 0): {
            (1, 2): [(6, 1), (4, 3), (2, 3)],
            (1, 6): [(6, 1), (4, 3), (2, 5)],
            (3, 4): [(6, 1), (4, 3)],
            (5, 2): [(6, 1)],
        }
    }

    assert expected == result


def test_should_return_true_when_white_king_capture_at_back_direction_is_available(game_engine):
    game_engine.cur_player = 1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {(3, 3): {(1, 1): [(2, 2)], (1, 5): [(2, 4)]}}

    assert expected == result


def test_should_return_true_when_white_king_multiple_captures_at_back_directions_are_available(game_engine):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[0][7].is_king = True
    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {
        (0, 7): {(6, 5): [(1, 6), (3, 4), (5, 4)], (4, 3): [(1, 6), (3, 4)], (4, 7): [(1, 6), (3, 6)], (2, 5): [(1, 6)]}
    }

    assert expected == result


def test_should_return_true_if_white_king_can_not_capture_own_player_pawns(game_engine):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[3][3].is_king = True
    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {}

    assert expected == result


def test_should_return_true_if_white_pawn_can_not_capture_backwards(game_engine):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[3][3].is_king = True
    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {(3, 3): {(5, 1): [(4, 2)], (5, 5): [(4, 4)]}}

    assert expected == result


def test_should_return_true_if_white_pawn_can_capture_at_given_directions(game_engine):
    game_engine.cur_player = 1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    row, col = 3, 3
    expected = True

    result_forw_left = game_engine._can_capture_at_direction(row, col, DIRECTIONS["forward_left"])
    result_forw_right = game_engine._can_capture_at_direction(row, col, DIRECTIONS["forward_right"])
    result_back_left = game_engine._can_capture_at_direction(row, col, DIRECTIONS["back_left"])
    result_back_right = game_engine._can_capture_at_direction(row, col, DIRECTIONS["back_right"])

    assert result_forw_left is expected
    assert result_forw_right is expected
    assert result_back_left is expected
    assert result_back_right is expected


def test_should_return_true_when_all_black_pawns_capture_moves_added_to_captures(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {(4, 3): {(6, 1): [(5, 2)], (6, 5): [(5, 4)]}}

    assert expected == result


def test_should_return_true_when_no_captures_are_available_for_black_pawn_at_the_board_edges(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix = [
        [Piece(1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0)],
        [Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1)],
        [Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1)],
        [Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0)],
        [Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1)],
        [Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0)],
        [Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1)],
        [Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0)],
    ]

    game_engine.find_available_capture_moves()
    result = game_engine.captures
    expected = {}

    assert expected == result


def test_should_return_true_when_black_king_pawn_can_not_capture_across_vertical_board_edges(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix = [
        [Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(1)],
    ]

    game_engine.matrix[1][2].is_king = True
    game_engine.matrix[6][6].is_king = True
    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {}

    assert expected == result


def test_should_return_true_when_all_black_pawn_captures_added_to_dictionary(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(-1), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(-1), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0)],
    ]

    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {
        (0, 2): {(2, 0): [(1, 1)], (6, 0): [(1, 3), (3, 3), (5, 1)], (4, 2): [(1, 3), (3, 3)], (2, 4): [(1, 3)]},
        (1, 5): {(5, 5): [(2, 6), (4, 6)], (3, 7): [(2, 6)]},
        (3, 5): {(5, 3): [(4, 4)], (5, 7): [(4, 6)]},
    }

    assert expected == result


def test_should_return_true_when_black_pawn_multiple_captures_are_available(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(-1), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {
        (0, 4): {
            (6, 2): [(1, 3), (3, 3), (5, 3)],
            (4, 0): [(1, 3), (3, 1)],
            (4, 4): [(1, 3), (3, 3)],
            (2, 2): [(1, 3)],
        },
        (1, 5): {(5, 5): [(2, 6), (4, 6)], (3, 7): [(2, 6)]},
    }

    assert expected == result


def test_should_return_true_when_black_king_capture_at_back_direction_is_available(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {(3, 3): {(5, 1): [(4, 2)], (5, 5): [(4, 4)]}}

    assert expected == result


def test_should_return_true_when_black_king_multiple_captures_at_back_directions_are_available(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1)],
    ]

    game_engine.matrix[7][7].is_king = True
    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {
        (7, 7): {
            (7, 3): [(6, 6), (4, 4), (4, 2), (6, 2)],
            (5, 1): [(6, 6), (4, 4), (4, 2)],
            (3, 3): [(6, 6), (4, 4)],
            (5, 5): [(6, 6)],
        }
    }

    assert expected == result


def test_should_return_true_if_black_king_can_not_capture_own_player_pawns(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[3][3].is_king = True
    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {}

    assert expected == result


def test_should_return_true_if_black_pawn_can_not_capture_backwards(game_engine):
    game_engine.cur_player = -1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[3][3].is_king = True
    game_engine.find_available_capture_moves()

    result = game_engine.captures
    expected = {(3, 3): {(5, 1): [(4, 2)], (5, 5): [(4, 4)]}}

    assert expected == result


def test_should_return_true_if_black_pawn_can_capture_at_given_directions(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    row, col = 3, 3
    expected = True

    result_forw_left = game_engine._can_capture_at_direction(row, col, DIRECTIONS["forward_left"])
    result_forw_right = game_engine._can_capture_at_direction(row, col, DIRECTIONS["forward_right"])
    result_back_left = game_engine._can_capture_at_direction(row, col, DIRECTIONS["back_left"])
    result_back_right = game_engine._can_capture_at_direction(row, col, DIRECTIONS["back_right"])

    assert result_forw_left is expected
    assert result_forw_right is expected
    assert result_back_left is expected
    assert result_back_right is expected


def test_should_return_true_when_single_pawn_capture_moves_added_to_dictionary(game_engine):
    pawn_cords, capture_cords_left, move_to_cords_left = (0, 3), (1, 2), (2, 1)

    game_engine._add_capture_coordinates(pawn_cords, capture_cords_left, move_to_cords_left)

    result_left = game_engine.captures
    expected_left = {pawn_cords: {move_to_cords_left: capture_cords_left}}

    assert result_left == expected_left

    capture_cords_right, move_to_cords_right = (1, 4), (2, 5)

    game_engine._add_capture_coordinates(pawn_cords, capture_cords_right, move_to_cords_right)

    result_left_right = game_engine.captures
    expected_left_right = {
        pawn_cords: {move_to_cords_left: capture_cords_left, move_to_cords_right: capture_cords_right}
    }

    assert result_left_right == expected_left_right


def test_should_return_true_when_multiple_pawn_capture_moves_added_to_dictionary(game_engine):
    pawn_cords, capture_cords, move_to_cords = (0, 5), [(1, 4), (3, 2)], (4, 1)

    game_engine._add_capture_coordinates(pawn_cords, capture_cords, move_to_cords)

    result = game_engine.captures
    expected = {pawn_cords: {move_to_cords: capture_cords}}

    assert result == expected
