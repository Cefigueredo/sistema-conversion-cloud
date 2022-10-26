from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from enum import Enum
import os
import logging

LOGGER = logging.getLogger(__name__)

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    conversion_tasks = db.relationship(
        "ConversionTask", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all():
        return User.query.all()


class TaskStatus(Enum):
    UPLOADED = "UPLOADED"
    PROCESSED = "PROCESSED"


class TaskFormats(Enum):
    MP3 = "MP3"
    OGG = "OGG"
    WMA = "WMA"


class ConversionTask(db.Model):
    __tablename__ = "conversion_task"
    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow())
    finished_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String, default=TaskStatus.UPLOADED.value)
    user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    file_name = db.Column(db.String(150), nullable=False)
    new_file_format = db.Column(db.Enum(TaskFormats), nullable=False)

    def __init__(self, file_name, user_id, new_file_format) -> None:
        self.file_name = file_name
        self.user = user_id
        self.new_file_format = new_file_format

    def __repr__(self):
        return f"<Conversion Task {self.id} for user {self.user}>"

    @staticmethod
    def get_by_id(id):
        return ConversionTask.query.get(id)

    @staticmethod
    def get_all():
        return ConversionTask.query.all()

    @staticmethod
    def delete_file(path):
        if os.path.exists(path):
            os.remove(path)
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        includde_relationships = True
        load_instance = True


class ConversionTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ConversionTask
        includde_relationships = True
        load_instance = True
