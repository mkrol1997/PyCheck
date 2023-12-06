import os

from chatapp import create_app, db
from chatapp.constants import DB_PATH
from chatapp import socketio


def create_db(flask_app):
    with flask_app.app_context():
        if not os.path.exists(DB_PATH):
            db.create_all()


if __name__ == "__main__":
    app = create_app()
    create_db(app)

    socketio.run(app=app, host="127.0.0.1", port=8000)