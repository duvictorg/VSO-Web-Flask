"""
Routes and views for the flask application.
"""

from flask import render_template, jsonify, request, Blueprint,session,redirect,url_for
import requests
from markupsafe import escape
from VSO_Web_Flask import controller
from VSO_Web_Flask.controller import AuthenticationController




class AuthenticationViews:
    def __init__(self):
        self.auth_bp = Blueprint("auth_bp", __name__)
        self.controller = AuthenticationController()
        self.register_routes()


    def register_routes(self):

        @self.auth_bp.route("/", methods=["GET", "POST"])
        @self.auth_bp.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                username = request.form.get("username")
                password = request.form.get("password")
                result = self.controller.login(username, password)
                if "error" in result:
                    return render_template(
                        "index.html", message=result["error"]
                    )
                
                if result["role"] == 0:
                    return redirect(url_for("student_bp.student_details"))
                if result["role"] == 1:
                    return redirect(url_for("teacher_bp.teacher_details"))
            
                return redirect("/profile")
            return render_template("index.html")

        @self.auth_bp.route("/admin", methods=["GET", "POST"])
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

        @self.auth_bp.route("/logout")
        def logout():
            self.controller.logout()
            return redirect(url_for("auth_bp.login"))

        @self.auth_bp.route("/profile")
        def profile():
            if "user_id" in session:
                return f"Utilisateur {session['user_id']} est deja connecte"
            return "Pas d'utilisateur de connecte"