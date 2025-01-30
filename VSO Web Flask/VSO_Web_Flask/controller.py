from .user import UserModel
from flask import session

class AuthenticationController:
    def __init__(self):
        self.user_model = UserModel()

    def login(self,username,password):
        self.user_model.username = username
        user = self.user_model.get_user_by_username()
        if user and self.user_model.check_password(password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return {"success": "Connexion reussie", "Nom d'utilisateur": user['username'], "role": self.user_model.get_role()} 
        return {"error": "Nom d'utilisateur ou mot de passe incorrect"}

    def logout(self):
        session.clear()
        return {"success": "Deconnexion reussie"}

    def register(self,first_name,last_name,password,role,mail,matiere):
        r = self.user_model.create_user(first_name,last_name,password,role,matiere)
        return {"success": "Inscription reussie", "Nom d'utilisateur" : self.user_model.username} if r != False else {"error": "Personne deja existante"}

    def delete_account(self):
        pass

    def change_password(self):
        pass

    def list_grades(self):
        pass

    def list_students(self):
        pass

    def search_student(self):
        pass

    def add_grade(self):
        pass

    def delete_grade(self):
        pass

    def change_grade(self):
        pass

    def change_maximum_grade(self):
        pass

    def change_info_grade(self):
        pass

    def change_class(self):
        pass

    def change_mail(self):
        pass

    def get_info_student(self,id):
        pass

    def get_info_teacher(self,id):
        pass

