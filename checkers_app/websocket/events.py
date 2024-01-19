import random
import time

from flask import request
from flask_socketio import emit, join_room

from checkers_app.checkers.main import collection
from checkers_app.database import db_tools
from checkers_app.game_engine import game_engine, games_storage
from checkers_app.mcts.mcts import MonteCarloTreeSearch
from checkers_app.websocket import socketio
from constant import MCTS_ITERATIONS


@socketio.on("user_connected")
def user_connected(data):
    channel = data.get("channel")
    db_tools.add_player(channel, request.sid)


@socketio.on("get_matrix")
def send_matrix(data):
    matrix = []
    channel = data.get("channel")
    channel_game = games_storage.get_channel_game(channel)

    if channel_game:
        for row in channel_game.board.matrix:
            matrix_row = []
            for pawn in row:
                matrix_row.append([pawn.value, pawn.is_king])
            matrix.append(matrix_row)

    emit("receive_matrix", {"matrix": matrix}, room=channel)


@socketio.on("get_available_moves")
def find_pawns_to_move(data):
    channel = data.get("channel")
    channel_game = games_storage.get_channel_game(channel)

    game_engine.update_pawns_with_legal_moves(game=channel_game)
    pawns_with_moves = game_engine.get_next_moves(game=channel_game)

    if pawns_with_moves is not None:
        return emit("available_moves", {"moves": pawns_with_moves}, room=channel, to=request.sid)

    status = "No more moves available"
    emit("game_finished", {"winner": channel_game.active_player * -1, "status": status}, room=channel, broadcast=True)
    games_storage.remove_game(channel)


@socketio.on("get_cords_after_move")
def find_pawn_moves(data):
    channel = data.get("channel")
    channel_game = games_storage.get_channel_game(channel)
    pawn_cords = tuple(map(lambda cord: int(cord), data.get("pawn")))

    if pawn_cords in list(channel_game.captures.keys()):
        move_pawn_to_cords = list(map(lambda square_cords: square_cords, channel_game.captures[pawn_cords]))
        emit("cords_after_move", {"square_cords": move_pawn_to_cords}, room=channel, to=request.sid)
    else:
        emit("cords_after_move", {"square_cords": channel_game.basic_moves[pawn_cords]}, room=channel, to=request.sid)


@socketio.on("make_move")
def move_pawn(data):
    channel = data.get("channel")
    channel_game = games_storage.get_channel_game(channel)
    from_cords = tuple(map(lambda x: int(x), (data.get("from_cords").split("-"))))
    to_cords = tuple(map(lambda x: int(x), (data.get("to_cords").split("-"))))

    game_engine.move_pawn(channel_game, from_cords, to_cords)

    if from_cords in channel_game.captures.keys():
        capture_pawn_cords = channel_game.captures[from_cords][to_cords]
        game_engine.make_pawn_capture(channel_game, capture_pawn_cords)
    game_engine.switch_active_player(game=channel_game)

    current_player_sid = db_tools.current_player_sid(channel, channel_game.active_player)
    game_document = collection.find_one({"channel": channel})

    if game_document and channel_game and len(game_document.get("players")) == 2:
        return socketio.emit("play_game", room=current_player_sid)
    return play_ai_game({"channel": channel})


@socketio.on("join_room")
def join_game_room(data):
    channel = data.get("room_id")
    join_room(channel)
    emit("handle_message", f"{request.sid} has joined the room", room=channel, broadcast=True)


@socketio.on("play_game")
def play_checkers(data):
    channel = data.get("channel")
    channel_game = games_storage.get_channel_game(channel)
    game_document = collection.find_one({"channel": channel})

    if game_document and channel_game and len(game_document.get("players")) == 2:
        current_player_sid = db_tools.current_player_sid(channel, channel_game.active_player)
        socketio.emit("play_game", room=current_player_sid)


@socketio.on("disconnect")
def disconnect():
    user_sid = request.sid
    status = "Your opponent left"

    try:
        channels = socketio.server.manager.get_rooms(sid=user_sid, namespace="/")
        room_channel = next(filter(lambda channel: len(channel) == 8, channels))
        winner = db_tools.get_current_player(room_channel, user_sid) * -1

    except StopIteration:
        return
    except TypeError:
        winner = False

    emit("handle_message", f"{request.sid} has left the room", room=room_channel, broadcast=True)
    if winner:
        games_storage.remove_game(room_channel)
        emit("game_finished", {"winner": winner, "status": status}, room=room_channel, broadcast=True)


@socketio.on("play_ai_game")
def play_ai_game(data):
    channel = data.get("channel")
    channel_game = games_storage.get_channel_game(channel)

    db_tools.get_current_player(channel, request.sid)

    if channel_game.active_player == 1:
        return socketio.emit("play_game", room=request.sid)

    game_engine.update_pawns_with_legal_moves(game=channel_game)
    pawns_with_legal_moves = game_engine.get_next_moves(game=channel_game)

    if not pawns_with_legal_moves:
        status = "No more moves available"
        emit(
            "game_finished", {"winner": channel_game.active_player * -1, "status": status}, room=channel, broadcast=True
        )
        games_storage.remove_game(channel)

    mcts = MonteCarloTreeSearch(initial_state=channel_game, iterations=MCTS_ITERATIONS)
    current_state = mcts.run()

    games_storage.current_games[channel] = current_state.state
    send_matrix({"channel": channel})

    return socketio.emit("play_game", room=request.sid)


@socketio.on("send_message")
def handle_new_message(data):
    channel = data.get("room")
    emit("handle_message", data.get("message"), room=channel, broadcast=True, include_self=False)
