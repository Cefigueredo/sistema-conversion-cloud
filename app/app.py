import os
from flask import Flask, send_file
from werkzeug.utils import safe_join
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import db
from views import SignUpView, SignInView, TasksView, TaskView, FileView

app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)


@api.representation("application/octet-stream")
def output_file(data, code, headers):
    filepath = safe_join(data["directory"], data["filename"])

    response = send_file(
        filename_or_fp=filepath,
        mimetype="application/octet-stream",
        as_attachment=True,
        attachment_filename=data["filename"],
    )
    return response


# --- API Endpoints --
api.add_resource(SignUpView, "/api/auth/signup")
api.add_resource(SignInView, "/api/auth/login")
api.add_resource(TasksView, "/api/tasks")
api.add_resource(TaskView, "/api/tasks/<int:id_task>")
api.add_resource(FileView, "/api/files/<string:filename>")
jwt = JWTManager(app)
