import imp
from pydoc import doc
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from models import db, User, UserSchema, ConversionTask, ConversionTaskSchema

user_schema = UserSchema()
conversion_task_schema = ConversionTaskSchema()

class SignInView(Resource):
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