from flask import session
from .db import Database
from hashlib import sha256

class UserModel:
    def __init__(self, username=""):
        self.db = Database(['localhost','root','Jyfkf596f!BYFZEHf58f65zf!','users'])
        self.username = username

    def insert_user(self, first_name, last_name, role, matiere, hashed_password):
        query = "INSERT INTO username (username, mail) VALUES (%(username)s, '')"
        params = {'username': self.username}

        self.db.execute(query, params)
        user_id = self.db.cursor.lastrowid

        query = "INSERT INTO passwords (id, password) VALUES (%(user_id)s, %(hashed_password)s)"
        params = {'user_id': user_id, 'hashed_password': hashed_password}

        self.db.execute(query, params)

        if role == 0:
            query = "INSERT INTO students (id, first_name, last_name) VALUES (%(user_id)s, %(first_name)s, %(last_name)s)"
            params = {'user_id': user_id, 'first_name': first_name, 'last_name': last_name}
        else:
            query = "INSERT INTO teachers (id, first_name, last_name, class) VALUES (%(user_id)s, %(first_name)s, %(last_name)s, %(matiere)s)"
            params = {'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'matiere': matiere}

        self.db.execute(query, params)


    def create_user(self, first_name, last_name, password, role, matiere):
        self.username = str(first_name+'.'+last_name[0])
        hashed_password = sha256(password.encode()).hexdigest()
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
            id_role = self.get_teacher_or_student_id()
            role = self.get_role()
            tables = ['passwords', 'students', 'teachers', 'grades', 'username']
            for table in tables:
                if table == 'grades':
                    query = "DELETE FROM grades WHERE student_id = %(id_role)s" if role == 0 else "DELETE FROM grades WHERE teacher_id = %(id_role)s"
                    params = {'id_role': id_role}
                else:
                    query = f"DELETE FROM {table} WHERE id = %(user_id)s"
                    params = {'user_id': user_id}

                self.db.execute(query, params)
            return True
        return False   

    def get_user_by_username(self):
        query = "SELECT * FROM username WHERE username = %(username)s"
        params = {'username': self.username}

        result = self.db.query(query, params)
        return result[0] if result else None

    def get_name(self):
        id_role = str(self.get_teacher_or_student_id())
        role = self.get_role()

        if id_role:
            if role == 0:
                query = "SELECT first_name, last_name FROM students WHERE student_id = %(id_role)s"
            else:
                query = "SELECT first_name, last_name FROM teachers WHERE teacher_id = %(id_role)s"
    
            params = {'id_role': id_role}
            result = self.db.query(query, params)

        return (result[0]['first_name'], result[0]['last_name']) if result else None

    def check_password(self, password):
        user = self.get_user_by_username()
        if user:
            query = "SELECT password FROM passwords WHERE id = %(user_id)s"
            params = {'user_id': user['id']}
            result = self.db.query(query, params)

            if sha256(password.encode()).hexdigest() == result[0]['password']:
                return True
            else:
                return False
        return False

    def get_role(self):
        user_id = self.get_user_by_username()
        if user_id:
            query = "SELECT * FROM students WHERE id = %(user_id)s"
            params = {'user_id': user_id['id']}
            result = self.db.query(query, params)

            if result:
                return 0
            else:
                return 1


    def get_teacher_or_student_id(self):
        user_id = self.get_user_by_username()
        if user_id:
            user_id = str(user_id['id'])
            role = self.get_role()

            if role == 0:
                query = "SELECT student_id FROM students WHERE id = %(user_id)s"
            else:
                query = "SELECT teacher_id FROM teachers WHERE id = %(user_id)s"
        
            params = {'user_id': user_id}
            result = self.db.query(query, params)

            return result[0][next(iter(result[0]))] if result else False

    def alter_password(self, password, new_password):
        if self.check_password(password) and new_password != password:
            query = "UPDATE passwords SET password = %(new_password)s WHERE id = %(user_id)s"
            params = {
                'new_password': sha256(new_password.encode()).hexdigest(),
                'user_id': self.get_user_by_username()['id']
            }
            self.db.execute(query, params)
            return True
        return False

    def add_grade(self, student_id, grade, max_grade, classe, informations, coef):
        query = """
        INSERT INTO grades (student_id, teacher_id, grade, max_grade, class, informations, coef)
        VALUES (%(student_id)s, %(teacher_id)s, %(grade)s, %(max_grade)s, %(classe)s, %(informations)s, %(coef)s)
        """
        params = {
            'student_id': student_id,
            'teacher_id': self.get_teacher_or_student_id(),
            'grade': grade,
            'max_grade': max_grade,
            'classe': classe,
            'informations': informations,
            'coef': coef
        }
        self.db.execute(query, params)


    def delete_grade():
        pass

    def get_grades():
        pass
    
    def alter_class(self, new_class, password):
        if self.check_password(password):
            query = "UPDATE teachers SET class = %(new_class)s WHERE id = %(user_id)s"
            params = {
                'new_class': new_class,
                'user_id': self.get_user_by_username()['id']
            }
            self.db.execute(query, params)
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

    def get_student_id_by_name(self, first_name, last_name):
        query = "SELECT student_id FROM students WHERE first_name = %(first_name)s AND last_name = %(last_name)s"
        params = {'first_name': first_name, 'last_name': last_name}
        result = self.db.query(query, params)
        return result[0]['student_id'] if result else False

    def get_class(self, id):
        query = "SELECT class FROM teachers WHERE id = %(id)s"
        params = {'id': id}
        result = self.db.query(query, params)
        return result[0]['class'] if result else False

    def get_grades(self, role_id):
        query = "SELECT grade, max_grade, class, informations, coef FROM grades WHERE student_id = %(role_id)s"
        params = {'role_id': role_id}
        result = self.db.query(query, params)
        return result if result else False

