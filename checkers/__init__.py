from datetime import timedelta
from hashlib import md5

from flask import Flask


def create_app():
    app = Flask(__name__)
    encryptor = md5()

    app.permanent_session_lifetime = timedelta(minutes=30)
    app.config["SECRET_KEY"] = encryptor.digest()
    app.config["DEBUG"] = True

    return app
