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
            classes = self.controller.list_teachers_classes(teacher_id)
            return render_template("teachers.html", classes=classes)
        
        @self.teacher_bp.route("/list")
        def list_teachers():
            teachers = self.controller.list_teachers()
            return render_template("teachers_add.html")

        @self.teacher_bp.route("/grades/<int:id>")
        def add_grades(id):
            teacher_id = session.get("user_id")
            teacher = self.controller.get_info_teacher(teacher_id)
            if "error" in teacher:
                return redirect(url_for("auth_bp.login"))
            return render_template("teachers_add.html")

        @self.teacher_bp.route("/classe/<int:id>")
        def teacher_students_classe(id):
            teacher_id = session.get("user_id")
            teacher = self.controller.get_info_teacher(teacher_id)
            if "error" in teacher:
                return redirect(url_for("auth_bp.login"))
            students = self.controller.list_students_classe(id)
            students_id = [D["id"] for D in students]
            Noms = [D["Nom"] for D in students]
            Prenoms = [D["Prenom"] for D in students]
            students_classes = [D["Classe"] for D in students]
            student_data = [
                {"id": id_, "Nom": nom, "Prenom": prenom, "Classe": classe}
                for id_, nom, prenom, classe in zip(students_id,Noms, Prenoms, students_classes)
            ]
            classes = self.controller.list_teachers_classes(teacher_id)
            return render_template("teachers_students_classe.html", student_data=student_data)
