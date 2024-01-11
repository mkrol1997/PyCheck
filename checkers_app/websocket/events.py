from flask import request
from flask_socketio import emit, join_room

from checkers_app.checkers.main import collection
from checkers_app.database import db_tools
from checkers_app.game_engine import games_storage
from checkers_app.websocket import socketio


@socketio.on("user_connected")
def user_connected(data):
    channel = data.get("channel")
    db_tools.add_player(channel, request.sid)


@socketio.on("get_matrix")
def send_matrix(data):
    matrix = []
    channel = data.get("channel")
    game = games_storage.get_channel_game(channel)

    if game:
        for row in game.matrix:
            matrix_row = []
            for pawn in row:
                matrix_row.append([pawn.value, pawn.is_king])
            matrix.append(matrix_row)

    emit("receive_matrix", {"matrix": matrix}, room=channel)


@socketio.on("get_available_moves")
def find_pawns_to_move(data):
    channel = data.get("channel")
    game = games_storage.get_channel_game(channel)

    game.update_pawns_with_legal_moves()
    pawns_with_moves = game.get_next_moves()

    if pawns_with_moves is not None:
        return emit("available_moves", {"moves": pawns_with_moves}, room=channel, to=request.sid)

    status = "No more available moves"
    emit("game_finished", {"winner": game.cur_player * -1, "status": status}, room=channel, broadcast=True)
    games_storage.remove_game(channel)


@socketio.on("get_cords_after_move")
def find_pawn_moves(data):
    channel = data.get("channel")
    game = games_storage.get_channel_game(channel)
    pawn_cords = tuple(map(lambda cord: int(cord), data.get("pawn")))

    if pawn_cords in list(game.captures.keys()):
        move_pawn_to_cords = list(map(lambda square_cords: square_cords, game.captures[pawn_cords]))
        emit("cords_after_move", {"square_cords": move_pawn_to_cords}, room=channel, to=request.sid)
    else:
        emit("cords_after_move", {"square_cords": game.basic_moves[pawn_cords]}, room=channel, to=request.sid)


@socketio.on("make_move")
def move_pawn(data):
    channel = data.get("channel")
    game = games_storage.get_channel_game(channel)
    from_cords = tuple(map(lambda x: int(x), (data.get("from_cords").split("-"))))
    to_cords = tuple(map(lambda x: int(x), (data.get("to_cords").split("-"))))

    game.move_pawn(from_cords, to_cords)

    if from_cords in game.captures.keys():
        capture_pawn_cords = game.captures[from_cords][to_cords]
        game.make_pawn_capture(capture_pawn_cords)
    game.switch_active_player()

    current_player_sid = db_tools.current_player_sid(channel, game.cur_player)
    socketio.emit("play_game", room=current_player_sid)


@socketio.on("join_room")
def join_game_room(data):
    channel = data.get("room_id")
    game = games_storage.get_channel_game(channel)

    join_room(channel)
    emit("handle_message", f"{request.sid} has joined the room", room=channel, broadcast=True)

    game_data = collection.find_one({"channel": channel})
    players = game_data.get("players")

    if game and players and len(game_data.get("players")) == 2:
        current_player_sid = db_tools.current_player_sid(channel, game.cur_player)
        socketio.emit("play_game", room=current_player_sid)


@socketio.on("disconnect")
def disconnect():
    user_sid = request.sid
    status = "Your opponent left"

    try:
        channels = socketio.server.manager.get_rooms(sid=user_sid, namespace="/")
        room_channel = next(filter(lambda channel: len(channel) == 8, channels))

    except StopIteration:
        return

    emit("handle_message", f"{request.sid} has left the room", room=room_channel, broadcast=True)

    winner = db_tools.get_current_player(room_channel, user_sid) * -1
    if winner:
        games_storage.remove_game(room_channel)
        emit("game_finished", {"winner": winner, "status": status}, room=room_channel, broadcast=True)


@socketio.on("send_message")
def handle_new_message(data):
    channel = data.get("room")
    emit("handle_message", data.get("message"), room=channel, broadcast=True)
