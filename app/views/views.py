from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from models import TaskStatus
from models import db, User, UserSchema, ConversionTask, ConversionTaskSchema
from datetime import datetime
from werkzeug.utils import secure_filename
import os

user_schema = UserSchema()
conversion_task_schema = ConversionTaskSchema()
FILES_FOLDER = os.getenv("FILES_FOLDER")


class SignUpView(Resource):
    def post(self):
        new_user = User(
            username=request.json["username"],
            email=request.json["email"],
            password=request.json["password"],
        )
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user.id)
        return {
            "mensaje": "User created successfully",
            "token": access_token,
            "id": new_user.id,
        }

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        user.password = request.json.get("password", user.password)
        db.session.commit()
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return "", 204


class SignInView(Resource):
    def post(self):
        usuario = User.query.filter(
            User.username == request.json["username"],
            User.password == request.json["password"],
        ).first()
        db.session.commit()
        if usuario is None:
            return "User does not exist", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Successfully signed in", "token": token_de_acceso}


class TasksView(Resource):
    @jwt_required()
    def post(self):
        message: str = ""
        status: int = 200
        file_to_upload = request.files["file"]
        new_format = request.form.get("new_format")
        try:
            if new_format == "mp3" or new_format == "wma" or new_format == "ogg":
                user_id = get_jwt_identity()
                new_task = ConversionTask(file_to_upload.filename, user_id, new_format)
                _save_file(file_to_upload, new_task.id, new_task.user)
                new_task.status = TaskStatus.UPLOADED.value
                new_task.save()
                db.session.add(new_task)
                db.commit()
                message = f"Tarea de conversión para archivo: {file_to_upload.filename} a formato {new_format} creada correctamente"
            else:
                message = f"Formato {new_format} no soportado. Los formatos soportados son: mp3, wma y ogg"
        except Exception as e:
            status = 500
            message = f"Error: {e}"
        time = datetime.now()
        return {"message": message, "status": status, "time": time}


def _save_file(uploaded_file, task_id, user_id):
    task = ConversionTask.get_by_id(task_id)

    if uploaded_file and uploaded_file.filename:
        try:
            file_name = secure_filename(uploaded_file.filename)
            file_path = os.path.join(f"{FILES_FOLDER}/{user_id}")
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            uploaded_file.save(os.path.join(f"{FILES_FOLDER}/{user_id}", file_name))
        except Exception as e:
            task.delete()
            raise Exception(f"Error uploading the file, please try again: {e}")
    else:
        raise Exception("File not provided")

    @jwt_required()
    def get(self):
        return [
            conversion_task_schema.dump(conversion_task)
            for conversion_task in ConversionTask.query.all()
        ]


class TaskView(Resource):
    @jwt_required()
    def get(self, id_task):
        return conversion_task_schema.dump(ConversionTask.query.get_or_404(id_task))

    @jwt_required()
    def put(self, id_task):
        message: str = ""
        status: int = 200
        task = ConversionTask.get_by_id(id_task)
        user_id = get_jwt_identity()
        new_format = request.form.get("new_format")

        try:
            if task.user != user_id:
                raise Exception(f"This user is not authorized")

            task.new_file_format = new_format
            task.status = TaskStatus.UPLOADED.value

            task.update()
            message = f"Task {id_task} correctly updated"

        except Exception as e:
            status = 500
            message = f"Error: {e}"

        return {"message": message, "status": status}

    @jwt_required
    def delete(self, id_task):
        message: str = ""
        status: int = 200
        task = ConversionTask.get_by_id(id_task)
        user_id = get_jwt_identity()

        try:
            if task.user != user_id:
                raise Exception(f"This user is not authorized")

            task.delete()
            message = f"Task {id_task} correctly deleted"

        except Exception as e:
            status = 500
            message = f"Error: {e}"

        return {"message": message, "status": status}


class FileView(Resource):
    @jwt_required
    def get(self, filename):
        return {"directory": "./files/", "filename": filename}
