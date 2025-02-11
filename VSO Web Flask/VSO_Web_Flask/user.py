from unittest import result
from flask import session
from .db import Database,encrypt_data,decrypt_data,encrypt_username,decrypt_username
import bcrypt

class UserModel:
    def __init__(self, username=""):
        self.db = Database()
        self.username = username

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_hashed_password(self, password, username):
        self.username = encrypt_username(username).decode()
        user_data = self.get_user_by_username()

        if not user_data:
            return False

        hashed_password = user_data['password']
        if not hashed_password:
            return False

        # Vérifier si le mot de passe est au format bytes ou string
        if type(hashed_password) == str:
            hashed_password = hashed_password.encode()  # S'assurer que c'est en bytes pour bcrypt
        return bcrypt.checkpw(password.encode(), hashed_password)


    def insert_user(self, first_name, last_name, role, classe_id, password, Mail):
        
        query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
        self.db.execute(query, (self.username, password))
        user_id = self.db.cursor.lastrowid
        if role == 0:
            query = "INSERT INTO Students (id, Nom, Prenom, Classe, Mail) VALUES (%s, %s, %s, %s, %s)"
            self.db.execute(query, (user_id, encrypt_data(last_name), encrypt_data(first_name), classe_id, encrypt_data(Mail)))
        else:
            query = "INSERT INTO Teachers (id, Nom, Prenom, Mail) VALUES (%s, %s, %s, %s)"
            self.db.execute(query, (user_id, encrypt_data(last_name), encrypt_data(first_name), encrypt_data(Mail)))
        
        return user_id

    def create_user(self,first_name,last_name,password,role,Mail,classe_id):
        if len(first_name) >= 63:
            first_name = first_name[:63]
            self.username = str(first_name[:29]+'.'+last_name[0])

        else:
            self.username = str(first_name+'.'+last_name[0])
        self.username = encrypt_username(self.username)

        if len(last_name) >= 63:
            last_name = last_name[:63]

        if len(Mail) >= 254:
            Mail = Mail[:254]
        
        if type(role) != int and role in ('0','1'):
            role = int(role)
        if role not in (0,1):
            return False

        if type(classe_id) != int:
            return False
        
        hashed_password = self.hash_password(password)
        
        if self.get_user_by_username() == None:
            self.username = encrypt_username(self.username)
            self.insert_user(first_name, last_name, role, classe_id, hashed_password, Mail)
        else:
            index = 2
            while self.get_user_by_username() != None:
                self.username = str(first_name+'.'+last_name[0] + str(index))
                index+=1
            self.username = encrypt_username(self.username)
            self.insert_user(first_name, last_name, role, classe_id, hashed_password, Mail)
        return self.db.cursor.lastrowid

    def delete_user(self,username):
        self.username = encrypt_username(username)
        print(self.username)
        user = self.get_user_by_username()
        if user:
            user_id = user['id']
            role = self.get_role()
            print(role)
            
            if role == 0:
                self.db.execute("DELETE FROM grades WHERE id_student = %s", (user_id,))
                self.db.execute("DELETE FROM students_matieres WHERE id_student = %s", (user_id,))
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

    def get_list_students_classe(self,classe_id):
        query = "SELECT Nom,Prenom FROM Students WHERE Classe = (%s):"
        result = self.db.query(query, (classe_id,))
        if result:
            for d in result:
                d['Nom'] = decrypt_data(d['Nom'])
                d['Prenom'] = decrypt_data(d['Prenom'])
            return result
        else:
            return False

    def get_teacher_classes(self,teacher_id):
        query = "SELECT id_classe FROM teachers_classes WHERE id_teacher = (%s);"
        result = self.db.query(query, (teacher_id,))
        return result if result else False

    def get_teacher_matieres(self,teacher_id):
        query = "SELECT id_matiere FROM teachers_matieres WHERE id_teacher = (%s);"
        result_temp = self.db.query(query, (teacher_id,))
        query = "SELECT Matiere FROM matieres WHERE id = (%s);"
        result = self.db.query(query, (result_temp,)) #possiblement à corriger
        return result if result else False

    def list_teachers(self):
        query = "SELECT * FROM teachers;"
        result = self.db.query(query)
        if result:
            for d in result:
                d['Nom'] = decrypt_data(d['Nom'])
                d['Prenom'] = decrypt_data(d['Prenom'])
                d['Mail'] = decrypt_data(d['Mail'])
            return result
        else:
            return False

    def list_students(self):
        query = "SELECT * FROM students;"
        result = self.db.query(query)
        if result:
            for d in result:
                d['Nom'] = decrypt_data(d['Nom'])
                d['Prenom'] = decrypt_data(d['Prenom'])
                d['Mail'] = decrypt_data(d['Mail'])
            return result
        else:
            return False

    def list_users_by_id(self,liste_id):
        query = "SELECT username FROM users WHERE id IN ({})".format(", ".join(map(str, liste_id)))
        result = self.db.query(query)
        return [decrypt_username(d['username']) for d in result] if result else []

    def list_matieres(self):
        return self.db.query("SELECT Matiere FROM matieres;")

    def list_matieres_by_id(self,liste_id):
        query = "SELECT Matiere FROM matieres WHERE id IN ({})".format(", ".join(map(str, liste_id)))
        result = self.db.query(query)
        return result if result else []

    def list_annees(self):
        return self.db.query("SELECT Annee FROM classes;")

    def list_numeros_classes(self):
        return self.db.query("SELECT Numero_Classe FROM classes;")

    def list_student_matieres(self,id_student):
        query = "SELECT id_matiere FROM students_matieres WHERE id_student = (%s);"
        result_temps = self.db.query(query, (id_student,))
        return result_temps if result_temps else False

    def get_id_classe(self,annee,numero_classe):
        query = "SELECT id FROM classes WHERE Annee = (%s) AND Numero_Classe = (%s);"
        result = self.db.query(query, (annee, numero_classe,))
        return result if result else None

    def get_id_matiere(self,matiere):
        query = "SELECT id FROM matieres WHERE Matiere = (%s);"
        result = self.db.query(query, (matiere,))
        return result if result else None

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
        id_role = str(session['user_id'])
        role = session['role']
        if id_role:
            if role == 0:
                query = "SELECT Nom, Prenom FROM students WHERE id = %(id_role)s;"
            else:
                query = "SELECT Nom, Prenom FROM teachers WHERE id = %(id_role)s;"
    
            params = {'id_role': id_role}
            result = self.db.query(query, params)
        return (decrypt_data(result[0]['Prenom']), decrypt_data(result[0]['Nom'])) if result else None