"""
Routes and views for the flask application.
"""

from flask import render_template, jsonify, request, Blueprint, session, redirect, url_for
import requests
from markupsafe import escape
from flask_wtf.csrf import generate_csrf
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
                csrf_token_form = request.form.get("csrf_token")
                csrf_token_session = session.get("_csrf_token")

                if not csrf_token_form or csrf_token_form != csrf_token_session:
                    return "Erreur CSRF detectee", 400  # Bloque les attaques CSRF

                username = request.form.get("username")
                password = request.form.get("password")
                result = self.controller.login(username, password)

                if "error" in result:
                    return render_template("index.html", message=result["error"], csrf_token=session["_csrf_token"])

                if result["role"] == 0:
                    return redirect(url_for("student_bp.student_details"))
                if result["role"] == 1:
                    return redirect(url_for("teacher_bp.teacher_details"))
                if result["role"] == 2:
                    return redirect(url_for("admin_bp.admin_details"))

                return redirect("/")

            return render_template("index.html", csrf_token=session["_csrf_token"])

        @self.auth_bp.route("/logout")
        def logout():
            self.controller.logout()
            return redirect(url_for("auth_bp.login"))

        @self.auth_bp.route("/profile")
        def profile():
            if "user_id" in session:
                return f"Utilisateur {session['user_id']} est deja connecte"
            return "Pas d'utilisateur de connecte"
