from .user import UserModel
from flask import session

class AuthenticationController:
    def __init__(self):
        self.user_model = UserModel()

    def login(self,username,password):
        self.user_model.username = username
        user = self.user_model.get_user_by_username()
        checkpass = self.user_model.check_hashed_password(password,username)
        if user and checkpass:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = self.user_model.get_role()
            return {"success": "Connexion reussie", "Nom d'utilisateur": user['username'], "role": session['role']} 
        return {"error": "Nom d'utilisateur ou mot de passe incorrect"}

    def logout(self):
        session.clear()
        return {"success": "Deconnexion reussie"}

    def register(self,first_name,last_name,password,role,mail,matiere):
        r = self.user_model.create_user(first_name,last_name,password,role,matiere, mail)
        return {"success": "Inscription reussie", "Nom d'utilisateur" : self.user_model.username} if r != False else {"error": "Personne deja existante"}

    def delete_account(self):
        self.user_model.delete_user()
        session.clear()
        return {"success": "Utilisateur efface"}

    def change_password(self):
        pass

    def list_grades(self):
        role_id = self.user_model.get_teacher_or_student_id()
        result = self.user_model.get_grades(role_id)
        return result if result != False else None

    def list_grades_matiere(self,id_matiere):
        role_id = self.user_model.get_teacher_or_student_id()
        result = self.user_model.get_grades(role_id,id_matiere)
        return result if result != False else None

    def list_grades_matiere(self,id_matiere):
        role_id = self.user_model.get_teacher_or_student_id()
        result = self.user_model.get_grades_matiere(role_id,id_matiere)
        return result if result != False else None

    def list_students_classe(self,id_classe):
        result = self.user_model.get_list_students_classe(id_classe)
        return result if result != False else None

    def list_student(self):
        result = self.user_model.list_students()
        return result if result != False else None

    def list_teachers_classes(self,id_classe):
        result = self.user_model.get_teacher_classes(id_classe)
        return result if result != False else None

    def list_teachers_maieres(self,id_matiere):
        result = self.user_model.get_teacher_classes(id_matiere)
        return result if result != False else None

    def list_teachers(self):
        result = self.user_model.list_teachers()
        return result if result != False else None

    def search_student(self):
        pass

    def add_grade(self,first_name_student,last_name_student,grade,max_grade,informations,coef):
        student_id = self.user_model.get_student_id_by_name(first_name_student,last_name_student)
        self.user_model.add_grade(student_id,grade,max_grade,session['matiere'],informations,coef)

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
        if "role" not in session:
            return {"error": "Utilisateur non autorise pour le role"}
        if session['role'] !=0:
            return {"error": "Utilisateur non autorise pour le role"}
        if "username" not in session:
            return {"error": "Utilisateur non connecte"}

        self.user_model.username = session["username"]
        
        f_l_name = self.user_model.get_name()
    
        if not f_l_name:
            return {"error": "Utilisateur non existant"}

        return {
            "username": self.user_model.username,
            "first_name": f_l_name[0],
            "last_name": f_l_name[1]
        }

    def get_info_teacher(self,id):
        if "role" not in session:
            return {"error": "Utilisateur non autorise pour le role"}
        if session['role'] !=1:
            return {"error": "Utilisateur non autorise pour le role"}
        if "username" not in session:
            return {"error": "Utilisateur non connecte"}

        self.user_model.username = session["username"]
        
        f_l_name = self.user_model.get_name()
    
        if not f_l_name:
            return {"error": "Utilisateur non existant"}

        return {
            "username": self.user_model.username,
            "first_name": f_l_name[0],
            "last_name": f_l_name[1]
        }

    def get_info_admin(self,id):
        if "role" not in session:
            return {"error": "Utilisateur non autorise pour le role"}
        if session['role'] !=2:
            return {"error": "Utilisateur non autorise pour le role"}
        if "username" not in session:
            return {"error": "Utilisateur non connecte"}

        self.user_model.username = session["username"]
        
        f_l_name = self.user_model.get_name()
    
        if not f_l_name:
            return {"error": "Utilisateur non existant"}

        return {
            "username": self.user_model.username}

