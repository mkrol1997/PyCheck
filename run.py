import os

from checkers_app.checkers import create_app, socketio

if __name__ == "__main__":
    app = create_app()
    socketio.run(app=app, host=os.getenv("FLASK_HOST"), port=os.getenv("FLASK_PORT"), allow_unsafe_werkzeug=True)
