from checkers import create_app, socketio

if __name__ == "__main__":
    app = create_app()
    socketio.run(app=app, host="127.0.0.1", port=8000)
