"""
The flask application package.
"""

from flask import Flask, session
from flask_wtf.csrf import generate_csrf, CSRFProtect
import os
from dotenv import load_dotenv
from VSO_Web_Flask.views.auth import AuthenticationViews
from VSO_Web_Flask.views.student_views import StudentViews
from VSO_Web_Flask.views.teacher_views import TeacherViews
from VSO_Web_Flask.views.admin_views import AdminViews

load_dotenv()

def create_app():
    app = Flask(__name__)
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

    @app.before_request
    def set_csrf_token():
        """ Assure que le jeton CSRF est present dans la session avant chaque requete uniquement s'il n'existe pas """
        if "_csrf_token" not in session:
            session["_csrf_token"] = generate_csrf()

    student_views = StudentViews()
    teacher_views = TeacherViews()
    auth_views = AuthenticationViews()
    admin_views = AdminViews()

    app.register_blueprint(student_views.student_bp, url_prefix="/students")
    app.register_blueprint(teacher_views.teacher_bp, url_prefix="/teachers")
    app.register_blueprint(auth_views.auth_bp, url_prefix="/")
    app.register_blueprint(admin_views.admin_bp, url_prefix="/admin")

    return app
