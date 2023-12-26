from flask_socketio import emit, join_room, send

from game_engine import engine
from game_engine.engine import Board, GameEngine
from websockets import socketio

board = Board()
engine = GameEngine(board)


@socketio.on("get_matrix")
def send_matrix():
    matrix = []

    for row in engine.matrix:
        matrix_row = []
        for pawn in row:
            matrix_row.append([pawn.value, pawn.is_king])
        matrix.append(matrix_row)

    emit("receive_matrix", {"matrix": matrix})


@socketio.on("get_available_moves")
def find_pawns_to_move():
    engine.update_pawns_with_legal_moves()
    pawns_with_moves = engine.get_next_moves()

    if pawns_with_moves:
        return emit("available_moves", {"moves": pawns_with_moves})

    emit("game_finished")


@socketio.on("get_cords_after_move")
def find_pawn_moves(data):
    pawn_cords = tuple(map(lambda cord: int(cord), data["pawn"]))
    if pawn_cords in list(engine.captures.keys()):
        move_pawn_to_cords = list(map(lambda square_cords: square_cords, engine.captures[pawn_cords]))
        emit("cords_after_move", {"square_cords": move_pawn_to_cords})
    else:

        emit("cords_after_move", {"square_cords": engine.basic_moves[pawn_cords]})


@socketio.on("make_move")
def move_pawn(data):
    from_cords = tuple(map(lambda x: int(x), (data["from_cords"].split("-"))))

    to_cords = tuple(map(lambda x: int(x), (data["to_cords"].split("-"))))
    engine.move_pawn(from_cords, to_cords)

    if from_cords in engine.captures.keys():
        capture_pawn_cords = engine.captures[from_cords][to_cords]
        engine.make_pawn_capture(capture_pawn_cords)

    engine.switch_active_player()
