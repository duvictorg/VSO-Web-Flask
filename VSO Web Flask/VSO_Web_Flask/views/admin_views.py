from re import M
from flask import Blueprint, render_template, request, session, redirect, url_for
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
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))
            return render_template("admin.html", admin=admin)

        @self.admin_bp.route("/list/students")
        def list_students():
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))
            students = self.controller.list_student()
            Noms = [D["Nom"] for D in students]
            Prenoms = [D["Prenom"] for D in students]
            student_ids = [D["id"] for D in students]
            Mails = [D["Mail"] for D in students]
            return render_template("admin_students.html",Noms=Noms,Prenoms=Prenoms,student_ids=student_ids,Mails=Mails)

        @self.admin_bp.route("/list/teachers")
        def list_teachers():
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))
            teachers = self.controller.list_teachers()
            Noms = [D["Nom"] for D in teachers]
            Prenoms = [D["Prenom"] for D in teachers]
            student_ids = [D["id"] for D in teachers]
            Mails = [D["Mail"] for D in teachers]
            return render_template("admin_teachers.html",Noms=Noms,Prenoms=Prenoms,student_ids=student_ids,Mails=Mails)

        @self.admin_bp.route("/register", methods=["GET", "POST"])
        def register():
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            print(admin)
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))
            if request.method == "POST":
                password = request.form.get("password")
                role = request.form.get("role")
                if role == None:
                    role = 0
                else:
                    role = int(role) 
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                mail = request.form.get("mail")
                matiere = request.form.get("matiere")
                result = self.controller.register(first_name,last_name,password,role,mail,matiere)
                if "error" in result:
                    return render_template(
                        "admin.html", message=result["error"]
                    )

                return redirect(url_for("auth_bp.login"))

            return render_template("admin-add.html")