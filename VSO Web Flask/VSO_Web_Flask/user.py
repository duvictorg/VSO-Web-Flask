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
            id_role = self.get_teacher_or_student_id(username)
            role = self.get_role(username)
            tables = ['passwords', 'students', 'teachers', 'grades', 'username']
            for table in tables:
                if table == 'grades':
                    self.db.execute("DELETE FROM grades WHERE student_id = '" + str(id_role) + "';") if role == 0 else self.db.execute("DELETE FROM grades WHERE teacher_id = '" + str(id_role) + "';")
                else:
                    self.db.execute("DELETE FROM " + table + " WHERE id = '" + str(user_id) + "';")
            return True
        return False   

    def get_user_by_username(self, username):
        result = self.db.query("SELECT * FROM username WHERE username = '"+ username + "';")
        return result[0] if result else None

    def get_name(self,username):
        id_role = str(self.get_teacher_or_student_id(username))
        role = self.get_role(username)
        if id_role:
            result = self.db.query("SELECT first_name,last_name FROM students WHERE student_id = " + id_role + ";") if role == 0 else self.db.execute("SELECT first_name,last_name FROM teachers WHERE teacher_id = " + id_role + ";")
        return (result[0]['first_name'], result[0]['last_name']) if result else None

    def check_password(self, username, password):
        user = self.get_user_by_username(username)
        if user:
            result = self.db.query("SELECT password FROM passwords WHERE id = " + str(user['id']) + ";")
            if sha256(password.encode()).hexdigest() == result[0]['password']:
                return True
            else:
                return False
        return False

    def get_role(self,username):
        user_id = self.get_user_by_username(username)
        if user_id:
            result = self.db.query("SELECT * FROM students WHERE id = " + str(user_id['id']) + ";")
            if result:
                return 0
            else:
                return 1

    def get_teacher_or_student_id(self,username):
        user_id = self.get_user_by_username(username)
        if user_id:
            user_id = str(user_id['id'])
            role = self.get_role(username)
            result = self.db.query("SELECT student_id FROM students WHERE id = ('" + user_id + "');")[0] if role == 0 else self.db.query("SELECT teacher_id FROM teachers WHERE id = ('" + user_id + "');")[0]
            return result[next(iter(result))] if result else False

    def alter_password(self, username, password ,new_password):
        if self.check_password(username,password) and new_password != password:
            self.db.execute("UPDATE passwords SET password = '" + sha256(new_password.encode()).hexdigest() + "' WHERE id = " + str(self.get_user_by_username(username)['id']) + ";")
            return True
        return False

    def add_grade():
        pass

    def delete_grade():
        pass

    def get_grades():
        pass
    
    def alter_class(self, username, new_class, password):
        if self.check_password(username,password):
            self.db.execute("UPDATE teachers SET class = '" + new_class + "' WHERE id = '" + str(self.get_user_by_username(username)['id']) + "';")
            return True
        return False


    def alter_grade():
        pass

    def alter_maximum_grade():
        pass

    def alter_coef():
        pass

    def alter_info_grade():
        pass
    
