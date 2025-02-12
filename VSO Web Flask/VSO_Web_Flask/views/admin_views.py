from re import M
from types import NoneType
from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_wtf.csrf import generate_csrf
from VSO_Web_Flask.controller import AuthenticationController

class AdminViews:
    def __init__(self):
        self.admin_bp = Blueprint("admin_bp", __name__)
        self.controller = AuthenticationController()
        self.register_routes()

    def register_routes(self):
        @self.admin_bp.route("/")
        def admin_details():
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            if type(admin) == NoneType:
                return redirect(url_for("auth_bp.login"))
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))
            return render_template("admin.html", admin=admin, csrf_token=session["_csrf_token"])

        @self.admin_bp.route("/list/students")
        def list_students():
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            if type(admin) == NoneType:
                return redirect(url_for("auth_bp.login"))
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))
            students = self.controller.list_students()
            Noms = [D["Nom"] for D in students]
            Prenoms = [D["Prenom"] for D in students]
            student_ids = [D["id"] for D in students]
            students_classes = [D["Classe"] for D in students]
            Matieres = [self.controller.list_student_matieres(student_id) for student_id in student_ids]
            student_data = [
                {"id": id_, "Nom": nom, "Prenom": prenom, "Classe": classe, "Matieres": matieres}
                for id_, nom, prenom, classe, matieres in zip(student_ids, Noms, Prenoms, students_classes, Matieres)
            ]
            return render_template("admin_students.html", student_data=student_data)

        @self.admin_bp.route("/list/teachers")
        def list_teachers():
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            if type(admin) == NoneType:
                return redirect(url_for("auth_bp.login"))
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))
            teachers = self.controller.list_teachers()
            Noms = [D["Nom"] for D in teachers]
            Prenoms = [D["Prenom"] for D in teachers]
            teacher_ids = [D["id"] for D in teachers]
            Classes = [self.controller.list_teachers_classes(id_teacher) for id_teacher in teacher_ids]
            Matieres = [self.controller.list_teachers_matieres(id_teacher) for id_teacher in teacher_ids]
            teacher_data = [
                {"id": id_, "Nom": nom, "Prenom": prenom, "Classes": classes, "Matieres": matieres}
                for id_, nom, prenom, classes, matieres in zip(teacher_ids, Noms, Prenoms, Classes, Matieres)
            ]
            return render_template("admin_teachers.html", teacher_data=teacher_data)

        @self.admin_bp.route("/register", methods=["GET", "POST"])
        def register():
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))

            if request.method == "POST":
                csrf_token_form = request.form.get("csrf_token")
                csrf_token_session = session.get("_csrf_token")

                if not csrf_token_form or csrf_token_form != csrf_token_session:
                    return "Erreur CSRF détectée", 400  # Bloque les attaques CSRF

                action = request.form.get("action")

                if action == 'add':
                    password = request.form.get("password")
                    role = request.form.get("role")
                    if role is None:
                        role = 0
                    elif role in (0, 1):
                        role = int(role)
                    first_name = request.form.get("first_name")
                    last_name = request.form.get("last_name")
                    mail = request.form.get("mail")
                    annee = request.form.get("annee")
                    numero_classe = request.form.get("numero_classe")
                    matiere = request.form.get("matiere")

                    result = self.controller.register(first_name, last_name, password, role, mail, annee, numero_classe, matiere)
                    if "error" in result:
                        return render_template("admin.html", message=result["error"], csrf_token=session["_csrf_token"])

                    return redirect(url_for("admin_bp.register"))

                elif action == 'delete':
                    username = request.form.get('username')
                    print(username)
                    self.controller.delete_account(username)
                    return redirect(url_for("admin_bp.register"))

            teachers = self.controller.list_teachers()
            teachers = self.controller.list_users_by_id([d['id'] for d in teachers])
            eleves = self.controller.list_students()
            eleves = self.controller.list_users_by_id([d['id'] for d in eleves])
            matieres = self.controller.list_matieres()
            annees = list(set(self.controller.list_annees()))
            numeros = list(set(self.controller.list_numeros_classes()))

            return render_template("admin-add.html", teachers=teachers, eleves=eleves, matieres=matieres, annees=annees, numeros=numeros, csrf_token=session["_csrf_token"])

        @self.admin_bp.route("/modifier/student/<int:id>")
        def modifier_student(id):
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))

            return render_template("admin_students_modif.html")

        @self.admin_bp.route("/modifier/teacher/<int:id>")
        def modifier_teacher(id):
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))

            return render_template("admin_teachers_modif.html")
