import random

from flask import Blueprint, redirect, render_template, request, url_for

main = Blueprint("main", __name__)


@main.route("/home")
def test():
    return render_template("home.html")


@main.route("/room")
def room():
    room_id = random.randint(100000, 999999)
    pawn_black_url = url_for("static", filename="assets/board/pawn_black.png")
    pawn_white_url = url_for("static", filename="assets/board/pawn_white.png")

    return render_template("room.html", room=room_id, pawn_white=pawn_white_url, pawn_black=pawn_black_url)
