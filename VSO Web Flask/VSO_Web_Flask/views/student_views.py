from flask import Blueprint, render_template, request, session, redirect, url_for
from VSO_Web_Flask.controller import AuthenticationController

class StudentViews:
    def __init__(self):
        self.student_bp = Blueprint("student_bp", __name__)
        self.controller = AuthenticationController()
        self.register_routes()

    def register_routes(self):
        @self.student_bp.route("/me")
        def student_details():
            student_id = session.get("user_id")
            student = self.controller.get_info_student(student_id)
            if "error" in student:
                return redirect(url_for("auth_bp.login"))
            return render_template("student.html", student=student)

        @self.student_bp.route("/list")
        def list_grades():
            grades = self.controller.list_grades()
            return render_template("student.html", grades=grades)