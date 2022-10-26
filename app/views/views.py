import imp
from pydoc import doc
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from tasks import create_task
from models import db, User, UserSchema, ConversionTask, ConversionTaskSchema

user_schema = UserSchema()
conversion_task_schema = ConversionTaskSchema()

class SignUpView(Resource):
    def post(self):
        new_user = User(
            username=request.json["username"], email=request.json["email"], password=request.json["password"])
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user.id)
        return {"mensaje": "User created successfully", "token": access_token, "id": new_user.id}
    
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        user.password = request.json.get("password", user.password)
        db.session.commit()
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class SignInView(Resource):

    def post(self):
        usuario = User.query.filter(User.username == request.json["username"],
                                    User.password == request.json["password"]).first()
        db.session.commit()
        if usuario is None:
            return "User does not exist", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Successfully signed in", "token": token_de_acceso}

class TasksView(Resource):
    
    def post(self):
        content = request.json
        task_type = content["type"]
        task = create_task.delay(int(task_type))
        return jsonify({"task_id": task.id}), 202

class ConversionTask(Resource):

    def put(self, id_task):
        pass