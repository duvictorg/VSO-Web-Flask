from flask import Blueprint, render_template, request, session, redirect, url_for
from VSO_Web_Flask.controller import AuthenticationController

class AdminViews:
    def __init__(self):
        self.admin_bp = Blueprint("admin_bp", __name__)
        self.controller = AuthenticationController()
        self.register_routes()

    def register_routes(self):
        @self.admin_bp.route("/me")
        def admin_details():
            admin_id = session.get("user_id")
            admin = self.controller.get_info_admin(admin_id)
            if "error" in admin:
                return redirect(url_for("auth_bp.login"))
            return render_template("admin.html", admin=admin)

        @self.admin_bp.route("/list")
        def list_grades():
            grades = self.controller.list_grades()
            return render_template("admin.html", grades=grades)

        @self.admin_bp.route("/", methods=["GET", "POST"])
        @self.admin_bp.route("/register", methods=["GET", "POST"])
        def register():
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

            return render_template("admin.html")