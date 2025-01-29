from .db import Database
from hashlib import sha256

class UserModel:
    def __init__(self):
        self.db = Database(['localhost','root','Jyfkf596f!BYFZEHf58f65zf!','users'])

    def insert_user(self, first_name, last_name, role, matiere, hashed_password, username):
            self.db.execute("INSERT INTO username (username, mail) VALUES ('" + username + "','');")
            user_id = self.db.cursor.lastrowid

            self.db.execute("INSERT INTO passwords (id, password) VALUES ('" + str(user_id) + "', '" + hashed_password + "');")

            self.db.execute(str("INSERT INTO students (id,first_name,last_name) VALUES ('" + str(user_id) + "','" + first_name + "','" + last_name + "');" ) if role == 0 else str("INSERT INTO teachers (id,first_name,last_name,class) VALUES ('" + str(user_id) + "','" + first_name + "','" + last_name + "','" + matiere + "');"))


    def create_user(self, first_name, last_name, password, role, matiere):
        username = str(first_name+'.'+last_name[0])
        hashed_password = sha256(password.encode()).hexdigest()
        if self.get_user_by_username(username) == None:
            self.insert_user(first_name, last_name, role, matiere, hashed_password, username)

        elif self.get_name(first_name,last_name, role) == None:
            index = 2
            while self.get_user_by_username(username) != None:
                username = str(first_name+'.'+last_name[0] + str(index))
                index+=1
            self.insert_user(first_name, last_name, role, matiere, hashed_password, username)
        return self.db.cursor.lastrowid

    def delete_user(self, username):
        user = self.get_user_by_username(username)
        if user:
            user_id = user['id']
            role_check = self.db.query("SELECT id FROM students WHERE id = '" + str(user_id) + "';")
            column = 'student_id' if role_check else 'teacher_id'
        
            tables = ['passwords', 'students', 'teachers', 'grades', 'username']
            for table in tables:
                if table == 'grades':
                    self.db.execute("DELETE FROM " + table + " WHERE " + column + " = '" + str(user_id) + "';")
                else:
                    self.db.execute("DELETE FROM " + table + " WHERE id = '" + str(user_id) + "';")
            return True
        return False   

    def get_user_by_username(self, username):
        result = self.db.query("SELECT * FROM username WHERE username = '"+username + "';")
        return result[0] if result else None

    def get_name(self, first_name, last_name,role):
        result = self.db.query("SELECT * FROM students WHERE first_name = ('"+ first_name + "' AND last_name = '" + last_name +"');") if role == 0 else self.db.execute("SELECT * FROM teachers WHERE first_name = ('"+ first_name + "' AND last_name = '" + last_name +"');")
        return (result[2],result[3]) if result else None

    def check_password(self, username, password):
        user = self.get_user_by_username(username)
        if user and sha256(password.encode()).hexdigest():
            return True
        return False