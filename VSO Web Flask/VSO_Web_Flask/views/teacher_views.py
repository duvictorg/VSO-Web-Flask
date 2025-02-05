from flask import Blueprint, render_template, request, session, redirect, url_for

from VSO_Web_Flask.controller import AuthenticationController

class TeacherViews:
    def __init__(self):
        self.teacher_bp = Blueprint("teacher_bp", __name__)
        self.controller = AuthenticationController()
        self.register_route()

    def register_route(self):
        @self.teacher_bp.route("/me")
        def teacher_details():
            teacher_id = session.get("user_id")
            teacher = self.controller.get_info_teacher(teacher_id)
            if "error" in teacher:
                return redirect(url_for("auth_bp.login"))
            return render_template("main.html", teacher=teacher)
        
        @self.teacher_bp.route("/list")
        def list_teachers():
            teachers = self.controller.list_teachers()
            return render_template("main.html")

        @self.teacher_bp.route("/grades/add" ,methods=['POST'])
        def add_grades():
            if request.method == 'POST':
                result = self.controller.add_grade()
                return render_template("main.html")
