"""
The flask application package.
"""

from flask import Flask

from VSO_Web_Flask.views.auth import AuthenticationViews
from VSO_Web_Flask.views.student_views import StudentViews
from VSO_Web_Flask.views.teacher_views import TeacherViews

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = ("DevSecOps")

    student_views = StudentViews()
    teacher_views = TeacherViews()
    auth_views = AuthenticationViews()

    app.register_blueprint(student_views.student_bp, url_prefix="/students")
    app.register_blueprint(teacher_views.teacher_bp, url_prefix="/teachers")
    app.register_blueprint(auth_views.auth_bp, url_prefix="/")

    return app

