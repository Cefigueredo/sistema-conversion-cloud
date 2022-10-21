from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

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
class Status(enum.Enum):
    UPLOADED = 1
    PROCESSED = 2
    CD = 3


class ConversionTask(db.Model):
    __tablename__ = "conversion_task"
    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow())
    finished_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(10))
    user = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    input_file_id = db.relationship("File", uselist=False, backref="conversion_task")
    output_file_id = db.relationship("File", uselist=False, backref="conversion_task")

    def __repr__(self):
        return f"<Conversion Task {self.id} for user {self.user}>"

    @staticmethod
    def get_by_id(id):
        return ConversionTask.query.get(id)

    @staticmethod
    def get_all():
        return ConversionTask.query.all()


class File(db.Model):
    __tablename__ = "file"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    extension = db.Column(db.String(5))  # TODO add enum
    conversion_id = db.Column(db.Integer, db.ForeignKey("conversion_task.id"))
