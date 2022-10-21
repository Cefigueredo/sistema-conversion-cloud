from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging

LOGGER = logging.getLogger(__name__)
load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config[
        "SECRET_KEY"
    ] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app_context = app.app_context()
    app_context.push()
    db.init_app(app)
    from .models import User, ConversionTask, File

    db.create_all()
    return app
