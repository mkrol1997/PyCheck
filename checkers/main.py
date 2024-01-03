import uuid

from flask import Blueprint, render_template, url_for

main = Blueprint("main", __name__)


@main.route("/home")
def test():
    return render_template("home.html")


@main.route("/room")
def room():
    room_id = str(uuid.uuid4())[:8]

    assets = {
        "pawn_black": url_for("static", filename="assets/board/pawn_black.png"),
        "pawn_black_king": url_for("static", filename="assets/board/pawn_black_king.png"),
        "pawn_white": url_for("static", filename="assets/board/pawn_white.png"),
        "pawn_white_king": url_for("static", filename="assets/board/pawn_white_king.png"),
    }

    return render_template("room.html", room=room_id, **assets)
