from flask_socketio import emit, join_room, send

from checkers.checkers_game import Board
from checkers.websocket import socketio
from checkers_engine.move_validator import Validator

board = Board()
engine = Validator(board.matrix)


@socketio.on("get_matrix")
def send_matrix():
    emit("receive_matrix", {"matrix": engine.matrix})


@socketio.on("find_pawns_to_move")
def find_pawns_to_move(data):
    pawns_to_move = engine.find_pawns_available_to_move(data["current_player"])
    emit("found_legal_pawns", {"pawns_cords": pawns_to_move})


@socketio.on("find_pawn_moves")
def find_pawn_moves(data):
    pawn_legal_moves = engine.find_pawn_legal_moves(player=data["current_player"], pawn_cords=data["pawn"])

    emit("found_pawn_moves", {"pawns_cords": pawn_legal_moves})


@socketio.on("make_move")
def move_pawn(data):
    from_row, from_col = map(lambda x: int(x), (data["from_cords"].split("-")))
    to_row, to_col = map(lambda x: int(x), (data["to_cords"].split("-")))

    engine.matrix[from_row][from_col], engine.matrix[to_row][to_col] = (
        engine.matrix[to_row][to_col],
        engine.matrix[from_row][from_col],
    )


@socketio.on("find_pawns_to_capture")
def find_pawns_to_capture(data):
    curr_player = data["player"]
    pawns_to_capture = engine.find_pawns_to_capture(player=curr_player)
    socketio.emit("pawns_to_capture", {"pawns_to_capture": pawns_to_capture})


@socketio.on("find_pawn_capture_cords")
def find_pawn_capture_cords(data):
    curr_player = data["player"]
    capture_cords = engine.get_capture_cords(player=curr_player, pawn_cords=data["pawn"])

    emit("found_pawn_captures", {"capture_cords": capture_cords})


@socketio.on("make_capture")
def make_pawn_capture(data):
    from_row, from_col = map(lambda x: int(x), (data["from_cords"].split("-")))
    to_row, to_col = map(lambda x: int(x), (data["to_cords"].split("-")))

    engine.matrix[from_row][from_col], engine.matrix[to_row][to_col] = (
        engine.matrix[to_row][to_col],
        engine.matrix[from_row][from_col],
    )
    remove_piece_row = int((from_row + to_row) / 2)
    remove_piece_column = int((from_col + to_col) / 2)
    engine.matrix[remove_piece_row][remove_piece_column] = 0
