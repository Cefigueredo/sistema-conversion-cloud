from datetime import datetime
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dotenv import load_dotenv
import os
import logging

LOGGER = logging.getLogger(__name__)
load_dotenv()

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    conversion_tasks = db.relationship('ConversionTask', cascade='all, delete, delete-orphan')

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


# TODO add status enum to conversion task
class TaskStatus(Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    UPLOADED = 'UPLOADED'
    PROCESSED ='PROCESSED'


class ConversionTask(db.Model):
    __tablename__ = "conversion_task"
    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow())
    finished_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(10), default=TaskStatus.IN_PROGRESS.value)
    user = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    def __repr__(self):
        return f"<Conversion Task {self.id} for user {self.user}>"

    @staticmethod
    def get_by_id(id):
        return ConversionTask.query.get(id)

    @staticmethod
    def get_all():
        return ConversionTask.query.all()

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
