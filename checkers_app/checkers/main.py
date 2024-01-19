import uuid
from urllib.parse import urljoin

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from checkers_app.database import db
from checkers_app.game_engine import games_storage

collection = db.rooms
main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/create_room")
def create_room():
    channel = str(uuid.uuid4())[:8].upper()
    game_mode = request.args.get("game_mode")
    games_storage.add_new_game(channel)
    collection.insert_one({"channel": channel, "players": {}})

    game_modes = {
        "pvp": "main.room",
        "pve": "main.room_pve",
    }

    return redirect(url_for(game_modes[game_mode], channel=channel))


@main.route("/find_channel", methods=["POST"])
def find_channel():
    channel = request.get_json().get("channel").upper()
    channel_document = collection.find_one({"channel": channel})

    if channel_document:
        return jsonify(redirect_url=urljoin(request.url_root, url_for("main.room", channel=channel)), status=200)
    return jsonify(redirect_url=None, status=404)


@main.route("/room")
def room():
    channel = request.args.get("channel")
    join_url = urljoin(request.url_root, url_for("main.room", channel=channel))

    assets = {
        "pawn_black": url_for("static", filename="assets/board/pawn_black.png"),
        "pawn_black_king": url_for("static", filename="assets/board/pawn_black_king.png"),
        "pawn_white": url_for("static", filename="assets/board/pawn_white.png"),
        "pawn_white_king": url_for("static", filename="assets/board/pawn_white_king.png"),
        "board_img": url_for("static", filename="assets/board/board.png"),
    }
    if games_storage.get_channel_game(channel):
        return render_template("room.html", channel=channel, **assets, join_url=join_url)
    return redirect(url_for("main.home"))


@main.route("/room_pve")
def room_pve():
    channel = request.args.get("channel")
    join_url = urljoin(request.url_root, url_for("main.room", channel=channel))

    assets = {
        "pawn_black": url_for("static", filename="assets/board/pawn_black.png"),
        "pawn_black_king": url_for("static", filename="assets/board/pawn_black_king.png"),
        "pawn_white": url_for("static", filename="assets/board/pawn_white.png"),
        "pawn_white_king": url_for("static", filename="assets/board/pawn_white_king.png"),
        "board_img": url_for("static", filename="assets/board/board.png"),
    }

    if games_storage.get_channel_game(channel):
        return render_template("room_pve.html", channel=channel, **assets, join_url=join_url)
    return redirect(url_for("main.home"))
