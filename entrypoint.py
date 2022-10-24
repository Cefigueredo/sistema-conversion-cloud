import datetime
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import db
from views import SignUpView, SignInView

app = Flask(__name__)
app.config["SECRET_KEY"] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
# --- API Endpoints --
api.add_resource(SignUpView, '/signup')
api.add_resource(SignInView, '/signin')

jwt = JWTManager(app)
