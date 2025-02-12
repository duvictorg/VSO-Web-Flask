from types import NoneType
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
            if type(student) == NoneType:
                return redirect(url_for("auth_bp.login"))
            role_id = self.controller.get_role()
            matieres = self.controller.list_student_matieres(student_id)
            matieres = [D['Matiere'] for D in matieres]
            id_matieres = [self.controller.get_id_matiere(matiere) for matiere in matieres]
            dic_matieres =[
                {"id": id_, "Matiere": matiere}
                for id_, matiere in zip(id_matieres,matieres)
            ]
            if "error" in student:
                return redirect(url_for("auth_bp.login"))
            return render_template("student.html", student=student, matieres=dic_matieres)

        @self.student_bp.route("/grades/all")
        def list_grades():
            student_id = session.get("user_id")
            student = self.controller.get_info_student(student_id)
            if type(student) == NoneType:
                return redirect(url_for("auth_bp.login"))
            if "error" in student:
                return redirect(url_for("auth_bp.login"))
            grades = self.controller.list_grades()
            return render_template("student_grades.html", grades=grades)

        @self.student_bp.route("/grades/<int:id>")
        def modifier_student(id):
            student_id = session.get("user_id")
            student = self.controller.get_info_student(student_id)
            if type(student) == NoneType:
                return redirect(url_for("auth_bp.login"))
            grades = self.controller.list_grades_matiere(id)
            if "error" in student:
                return redirect(url_for("auth_bp.login"))
            return render_template("student_grades.html",grades=grades)