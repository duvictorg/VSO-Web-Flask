from flask import session
from .db import Database
import bcrypt

class UserModel:
    def __init__(self, username=""):
        self.db = Database(['localhost', 'pronote', 'pronote', 'ecole'])
        self.username = username

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_hashed_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def insert_user(self, first_name, last_name, role, classe_id, matieres, password):
        hashed_password = self.hash_password(password)
        
        query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
        self.db.execute(query, (self.username, hashed_password))
        user_id = self.db.cursor.lastrowid
        
        if role == 0:
            query = "INSERT INTO Students (id, Nom, Prenom, Classe) VALUES (%s, %s, %s, %s)"
            self.db.execute(query, (user_id, last_name, first_name, classe_id))
        else:
            query = "INSERT INTO Teachers (id, Nom, Prenom) VALUES (%s, %s, %s)"
            self.db.execute(query, (user_id, last_name, first_name))
            for matiere_id in matieres:
                query = "INSERT INTO Teachers_Matieres (id_teacher, id_matiere) VALUES (%s, %s)"
                self.db.execute(query, (user_id, matiere_id))
        
        return user_id

    def create_user(self, first_name, last_name, password, role, matiere):
        self.username = str(first_name+'.'+last_name[0])
        hashed_password = self.hash_password(password)
        if self.get_user_by_username() == None:
            self.insert_user(first_name, last_name, role, matiere, hashed_password)
        elif self.get_name() == None:
            index = 2
            while self.get_user_by_username() != None:
                self.username = str(first_name+'.'+last_name[0] + str(index))
                index+=1
            self.insert_user(first_name, last_name, role, matiere, hashed_password)
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
        query = "INSERT INTO Grades (id_student, id_matiere, Grade) VALUES (%s, %s, %s)"
        self.db.execute(query, (student_id, matiere_id, grade))

    def get_role(self):
        user = self.get_user_by_username()
        if user:
            result = self.db.query("SELECT id FROM Students WHERE id = %s", (user['id'],))
            return 0 if result else 1
        return None
