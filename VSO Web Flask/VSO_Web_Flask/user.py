from flask import session
from .db import Database
import bcrypt

class UserModel:
    def __init__(self, username=""):
        self.db = Database()
        self.username = username

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_hashed_password(self, password, username):
        self.username = username
        user_data = self.get_user_by_username()

        if not user_data:
            return False

        hashed_password = user_data['password']
        if not hashed_password:
            return False

        # Vérifier si le mot de passe est au format bytes ou string
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode()  # S'assurer que c'est en bytes pour bcrypt
        return bcrypt.checkpw(password.encode(), hashed_password)


    def insert_user(self, first_name, last_name, role, classe_id, matieres, password, Mail):
        
        query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
        self.db.execute(query, (self.username, password))
        user_id = self.db.cursor.lastrowid
        if role == 0:
            query = "INSERT INTO Students (id, Nom, Prenom, Classe, Mail) VALUES (%s, %s, %s, %s, %s)"
            print("je fais role 0")
            self.db.execute(query, (user_id, last_name, first_name, classe_id, Mail))
        else:
            print("je fais role 1")
            query = "INSERT INTO Teachers (id, Nom, Prenom, Mail) VALUES (%s, %s, %s, %s)"
            self.db.execute(query, (user_id, last_name, first_name, Mail))
            """
            query = "INSERT INTO Teachers_Matieres (id_teacher, id_matiere) VALUES (%s, %s)"
            self.db.execute(query, (user_id, matiere_id))"""
        
        return user_id

    def create_user(self, first_name, last_name, password, role, matiere, Mail):
        self.username = str(first_name+'.'+last_name[0])
        hashed_password = self.hash_password(password)
        if self.get_user_by_username() == None:
            self.insert_user(first_name, last_name, role, 1, matiere, hashed_password, Mail)
        elif self.get_name() == None:
            index = 2
            while self.get_user_by_username() != None:
                self.username = str(first_name+'.'+last_name[0] + str(index))
                index+=1
            self.insert_user(first_name, last_name, role, 1, matiere, hashed_password, Mail)
        else:
            return False
        return self.db.cursor.lastrowid

    def delete_user(self):
        user = self.get_user_by_username()
        if user:
            user_id = user['id']
            role = self.get_role()
            
            if role == 0:
                self.db.execute("DELETE FROM Students WHERE id = %s", (user_id,))
            else:
                self.db.execute("DELETE FROM Teachers_Matieres WHERE id_teacher = %s", (user_id,))
                self.db.execute("DELETE FROM Teachers_Classes WHERE id_teacher = %s", (user_id,))
                self.db.execute("DELETE FROM Teachers WHERE id = %s", (user_id,))
            
            self.db.execute("DELETE FROM Users WHERE id = %s", (user_id,))
            return True
        return False

    def get_user_by_username(self):
        result = self.db.query("SELECT * FROM Users WHERE username = %s", (self.username,))
        return result[0] if result else None

    def alter_password(self, old_password, new_password):
        user = self.get_user_by_username()
        if user and self.check_hashed_password(old_password, user['password']):
            hashed_new_password = self.hash_password(new_password)
            self.db.execute("UPDATE Users SET password = %s WHERE id = %s", (hashed_new_password, user['id']))
            return True
        return False

    def add_grade(self, student_id, matiere_id, grade):
        query = "INSERT INTO Grades (id_student, id_matiere, Grade) VALUES (%s, %s, %s);"
        self.db.execute(query, (student_id, matiere_id, grade))

    def get_grades_matiere(self,student_id,matiere_id):
        query = "SELECT Grade FROM Grades WHERE id_student = (%s) AND id_matiere = (%s);"
        result = self.db.query(query, (student_id, matiere_id,))
        return result if result else False
    
    def get_grades(self,student_id):
        query = "SELECT Grade FROM Grades WHERE id_student = (%s);"
        result = self.db.query(query, (student_id,))
        return result if result else False

    def get_role(self):
        user = self.get_user_by_username()
        if user:
            result_student = self.db.query("SELECT id FROM Students WHERE id = %s", (user['id'],))
            result_teacher = self.db.query("SELECT id FROM Teachers WHERE id = %s", (user['id'],))
            if result_student:
                return 0
            elif result_teacher:
                return 1
            else:
                result_admin = self.db.query("SELECT id FROM Admins WHERE id = %s", (user['id'],))
                return 2 if result_admin else None

        return None

    def get_name(self):
        id_role = str(self.get_teacher_or_student_id())
        role = self.get_role()
        if id_role:
            if role == 0:
                query = "SELECT Nom, Prenom FROM students WHERE id = %(id_role)s"
            else:
                query = "SELECT Nom, Prenom FROM teachers WHERE id = %(id_role)s"
    
            params = {'id_role': id_role}
            result = self.db.query(query, params)
        return (result[0]['Prenom'], result[0]['Nom']) if result else None

    def get_teacher_or_student_id(self):
        user_id = self.get_user_by_username()
        if user_id:
            user_id = str(user_id['id'])
            role = self.get_role()
            if role == 0:
                query = "SELECT id FROM students WHERE id = %(user_id)s"
            else:
                query = "SELECT id FROM teachers WHERE id = %(user_id)s"
        
            params = {'user_id': user_id}
            result = self.db.query(query, params)
            return result[0][next(iter(result[0]))] if result else False

