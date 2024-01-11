import os
from datetime import timedelta

from dotenv import find_dotenv, load_dotenv
from flask import Flask

from checkers_app.websocket.events import socketio

load_dotenv(find_dotenv())


def create_app():
    app = Flask(__name__)

    app.permanent_session_lifetime = timedelta(minutes=float(os.getenv("SESSION_TIMEOUT")))
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["MONGO_URI"] = f"{os.getenv('DATABASE_URI')}/{os.getenv('DATABASE_NAME')}"
    app.config["DEBUG"] = True

    socketio.init_app(app)

    from .main import main

    app.register_blueprint(main)

    return app
