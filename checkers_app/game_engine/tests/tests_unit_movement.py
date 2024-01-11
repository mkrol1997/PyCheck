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


def test_should_return_true_if_regular_white_pawn_can_move_forward_to_empty_square_at_given_direction(game_engine):
    game_engine.cur_player = 1

    result_left = game_engine._can_move_to_direction(row=5, column=2, direction=DIRECTIONS["forward_left"])
    result_right = game_engine._can_move_to_direction(row=5, column=2, direction=DIRECTIONS["forward_right"])

    expected = True

    assert expected is result_left
    assert expected is result_right


def test_should_return_true_if_regular_black_pawn_can_move_forward_to_empty_square_at_given_direction(game_engine):
    game_engine.cur_player = -1

    result_left = game_engine._can_move_to_direction(row=2, column=3, direction=DIRECTIONS["forward_left"])
    result_right = game_engine._can_move_to_direction(row=2, column=3, direction=DIRECTIONS["forward_right"])

    expected = True

    assert expected is result_left
    assert expected is result_right


def test_should_return_false_if_regular_white_pawn_can_not_move_forward_to_occupied_square_at_given_direction(
    game_engine,
):
    game_engine.cur_player = 1

    result_left = game_engine._can_move_to_direction(row=7, column=4, direction=DIRECTIONS["forward_left"])
    result_right = game_engine._can_move_to_direction(row=7, column=4, direction=DIRECTIONS["forward_right"])

    expected = False

    assert expected is result_left
    assert expected is result_right


def test_should_return_true_if_regular_black_pawn_can_not_move_forward_to_occupied_square_at_given_direction(
    game_engine,
):
    game_engine.cur_player = -1

    result_left = game_engine._can_move_to_direction(row=0, column=3, direction=DIRECTIONS["forward_left"])
    result_right = game_engine._can_move_to_direction(row=0, column=3, direction=DIRECTIONS["forward_right"])

    expected = False

    assert expected is result_left
    assert expected is result_right


def test_should_return_false_if_regular_white_pawn_can_not_move_backwards_to_occupied_square_at_given_direction(
    game_engine,
):
    game_engine.cur_player = 1

    result_left = game_engine._can_move_to_direction(row=5, column=2, direction=DIRECTIONS["back_left"])
    result_right = game_engine._can_move_to_direction(row=5, column=2, direction=DIRECTIONS["back_right"])

    expected = False

    assert expected is result_left
    assert expected is result_right


def test_should_return_true_if_regular_black_pawn_can_not_move_backwards_to_occupied_square_at_given_direction(
    game_engine,
):
    game_engine.cur_player = -1

    result_left = game_engine._can_move_to_direction(row=2, column=3, direction=DIRECTIONS["back_left"])
    result_right = game_engine._can_move_to_direction(row=2, column=3, direction=DIRECTIONS["back_right"])

    expected = False

    assert expected is result_left
    assert expected is result_right


def test_should_return_false_if_white_king_pawn_can_not_move_to_occupied_square_at_given_direction(game_engine):
    game_engine.cur_player = 1
    game_engine.matrix[6][1].is_king = True

    result_forward_left = game_engine._can_move_to_direction(row=6, column=1, direction=DIRECTIONS["forward_left"])
    result_forward_right = game_engine._can_move_to_direction(row=6, column=1, direction=DIRECTIONS["forward_right"])
    result_back_left = game_engine._can_move_to_direction(row=6, column=1, direction=DIRECTIONS["back_left"])
    result_back_right = game_engine._can_move_to_direction(row=6, column=1, direction=DIRECTIONS["back_right"])

    expected = False

    assert expected is result_forward_left
    assert expected is result_forward_right
    assert expected is result_back_left
    assert expected is result_back_right


def test_should_return_true_if_black_king_pawn_can_not_move_to_occupied_square_at_given_direction(game_engine):
    game_engine.cur_player = -1
    game_engine.matrix[1][2].is_king = True

    result_forward_left = game_engine._can_move_to_direction(row=1, column=2, direction=DIRECTIONS["forward_left"])
    result_forward_right = game_engine._can_move_to_direction(row=1, column=2, direction=DIRECTIONS["forward_right"])
    result_back_left = game_engine._can_move_to_direction(row=1, column=2, direction=DIRECTIONS["back_left"])
    result_back_right = game_engine._can_move_to_direction(row=1, column=2, direction=DIRECTIONS["back_right"])

    expected = False

    assert expected is result_forward_left
    assert expected is result_forward_right
    assert expected is result_back_left
    assert expected is result_back_right


def test_should_return_true_if_white_regular_pawn_moved_to_empty_forward_left_square(game_engine):
    game_engine.cur_player = 1
    move_from, move_to = (5, 2), (4, 1)

    game_engine.move_pawn(from_cords=move_from, to_cords=move_to)

    assert game_engine.matrix[4][1].value == 1
    assert game_engine.matrix[5][2].value == 0


def test_should_return_true_if_white_regular_pawn_moved_to_empty_forward_right_square(game_engine):
    game_engine.cur_player = 1
    move_from, move_to = (5, 4), (4, 5)

    game_engine.move_pawn(from_cords=move_from, to_cords=move_to)

    assert game_engine.matrix[4][5].value == 1
    assert game_engine.matrix[5][4].value == 0


def test_should_return_true_if_black_regular_pawn_moved_to_empty_forward_left_square(game_engine):
    game_engine.cur_player = -1
    move_from, move_to = (2, 3), (3, 2)

    game_engine.move_pawn(from_cords=move_from, to_cords=move_to)

    assert game_engine.matrix[3][2].value == -1
    assert game_engine.matrix[2][3].value == 0


def test_should_return_true_if_black_regular_pawn_moved_to_empty_forward_right_square(game_engine):
    game_engine.cur_player = -1

    game_engine.move_pawn(from_cords=(2, 3), to_cords=(3, 4))

    assert game_engine.matrix[3][4].value == -1
    assert game_engine.matrix[2][3].value == 0


def test_should_return_true_when_all_white_regular_pawns_starting_moves_added_to_basic_moves(game_engine):
    game_engine.cur_player = 1

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(5, 0): [(4, 1)], (5, 2): [(4, 1), (4, 3)], (5, 4): [(4, 3), (4, 5)], (5, 6): [(4, 5), (4, 7)]}

    assert result == expected


def test_should_return_true_when_white_king_pawn_legal_moves_added_to_basic_moves(game_engine):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(-1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1)],
        [Piece(0), Piece(-1), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0)],
    ]

    game_engine.matrix[4][3].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(4, 3): [(3, 2), (3, 4), (5, 2), (5, 4)]}

    assert result == expected


def test_should_return_true_when_regular_white_pawn_legal_moves_added_to_basic_moves(game_engine):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[4][3].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(4, 3): [(3, 2), (3, 4), (5, 2), (5, 4)]}

    assert result == expected


def test_should_return_true_when_white_king_pawn_legal_moves_with_opponent_neighbour_added_to_basic_moves(game_engine):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[4][3].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(4, 3): [(3, 4), (5, 2)]}

    assert result == expected


def test_should_return_true_when_no_white_king_pawn_legal_moves_with_opponent_neighbour_added_to_basic_moves(
    game_engine,
):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[4][3].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves

    expected = {}

    assert result == expected


def test_should_return_true_when_white_king_pawn_legal_moves_with_player_neighbour_added_to_basic_moves(game_engine):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[4][3].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(3, 4): [(2, 3), (2, 5)], (4, 3): [(3, 2), (5, 4)], (5, 2): [(4, 1)]}

    assert result == expected


def test_should_return_true_when_white_king_pawn_has_valid_moves_in_one_dir_at_the_board_edge_added_to_basic_moves(
    game_engine,
):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[3][0].is_king = True
    game_engine.matrix[3][7].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(3, 0): [(2, 1), (4, 1)], (3, 7): [(2, 6), (4, 6)]}

    assert result == expected


def test_should_return_true_when_only_white_king_pawn_neighbour_pawns_legal_moves_added_to_basic_moves(game_engine):
    game_engine.cur_player = 1

    game_engine.matrix = [
        [Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(-1)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(-1)],
        [Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0)],
        [Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1)],
    ]

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(3, 2): [(2, 1), (2, 3)], (3, 4): [(2, 3), (2, 5)], (5, 2): [(4, 1)], (5, 4): [(4, 5)]}

    assert result == expected


def test_should_return_true_when_all_black_regular_pawns_starting_moves_added_to_basic_moves(game_engine):
    game_engine.cur_player = -1

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(2, 1): [(3, 0), (3, 2)], (2, 3): [(3, 2), (3, 4)], (2, 5): [(3, 4), (3, 6)], (2, 7): [(3, 6)]}

    assert result == expected


def test_should_return_true_when_black_king_pawn_legal_moves_added_to_basic_moves(game_engine):
    game_engine.cur_player = -1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(1)],
        [Piece(0), Piece(1), Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0)],
    ]

    game_engine.matrix[4][3].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(4, 3): [(5, 2), (5, 4), (3, 2), (3, 4)]}

    assert result == expected


def test_should_return_true_when_regular_black_pawn_legal_moves_added_to_basic_moves(game_engine):
    game_engine.cur_player = -1

    game_engine.matrix = [
        [Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(0, 1): [(1, 0), (1, 2)], (4, 1): [(5, 0), (5, 2)], (4, 3): [(5, 2), (5, 4)], (4, 5): [(5, 4), (5, 6)]}

    assert result == expected


def test_should_return_true_when_black_king_pawn_legal_moves_with_opponent_neighbour_added_to_basic_moves(game_engine):
    game_engine.cur_player = -1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[4][3].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(4, 3): [(5, 2), (3, 4)]}

    assert result == expected


def test_should_return_true_when_no_black_king_pawn_legal_moves_with_opponent_neighbour_added_to_basic_moves(
    game_engine,
):
    game_engine.cur_player = -1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[4][3].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {}

    assert result == expected


def test_should_return_true_when_black_king_pawn_legal_moves_with_player_neighbour_added_to_basic_moves(game_engine):
    game_engine.cur_player = -1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[4][3].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(3, 4): [(4, 5)], (4, 3): [(5, 4), (3, 2)], (5, 2): [(6, 1), (6, 3)]}

    assert result == expected


def test_should_return_true_when_only_black_king_pawn_neighbour_pawns_legal_moves_added_to_basic_moves(game_engine):
    game_engine.cur_player = -1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(-1), Piece(0), Piece(-1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(3, 2): [(4, 1)], (3, 4): [(4, 5)], (5, 2): [(6, 1), (6, 3)], (5, 4): [(6, 3), (6, 5)]}

    assert result == expected


def test_should_return_true_when_black_king_pawn_has_valid_moves_in_one_dir_at_the_board_edge_added_to_basic_moves(
    game_engine,
):
    game_engine.cur_player = -1

    game_engine.matrix = [
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(-1), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0), Piece(-1)],
        [Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(1), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
        [Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
    ]

    game_engine.matrix[3][0].is_king = True
    game_engine.matrix[3][7].is_king = True

    game_engine.find_available_basic_moves()

    result = game_engine.basic_moves
    expected = {(3, 0): [(4, 1), (2, 1)], (3, 7): [(4, 6), (2, 6)]}

    assert result == expected


def test_should_return_true_when_pawn_moves_added_to_dictionary(game_engine):
    row, column, direction = 5, 2, DIRECTIONS["forward_right"]

    game_engine._add_move_coordinates(row, column, direction)

    result_right = game_engine.basic_moves
    expected_right = {(row, column): [(4, 3)]}

    assert result_right == expected_right

    direction = DIRECTIONS["forward_left"]
    game_engine._add_move_coordinates(row, column, direction)

    result_left_right = game_engine.basic_moves
    expected_left_right = {(row, column): [(4, 3), (4, 1)]}

    assert result_left_right == expected_left_right
