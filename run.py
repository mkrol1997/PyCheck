from checkers_app.checkers import create_app, socketio

if __name__ == "__main__":
    app = create_app()
    socketio.run(app=app, host="0.0.0.0", port=8000, allow_unsafe_werkzeug=True)
