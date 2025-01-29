from hashlib import sha256
import mysql.connector
from mysql.connector import Error

# Fonction pour se connecter à la base de données
# Retourne un objet connexion si la connexion est réussie, sinon None
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ntm.org",
            database="users"
        )

        if connection.is_connected():
            print("Connexion reussie a la base de donnees 'users'.")
            return connection
    except Error as e:
        print(f"Erreur lors de la connexion a la base de donnees : {e}")
        return None

# Fonction pour créer un utilisateur avec un mot de passe hashé
# username : Nom d'utilisateur
# password : Mot de passe à hacher en SHA-256
# role : 0 pour élève, 1 pour enseignant
def create_user(username, password, role):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            hashed_password = sha256(password.encode()).hexdigest()
            
            # Insérer l'utilisateur dans la table username
            cursor.execute("INSERT INTO username (username, mail) VALUES (%s, '')", (username,))
            user_id = cursor.lastrowid
            
            # Insérer le mot de passe hashé dans la table passwords
            cursor.execute("INSERT INTO passwords (id, password) VALUES (%s, %s)", (user_id, hashed_password))
            
            # Assigner l'utilisateur à la table students ou teachers selon son rôle
            cursor.execute("INSERT INTO students (id) VALUES (%s)" if role == 0 else "INSERT INTO teachers (id) VALUES (%s)", (user_id,))
            
            connection.commit()
            print("Utilisateur cree avec succes.")
        except Error as e:
            print(f"Erreur lors de la creation de l'utilisateur : {e}")
        finally:
            cursor.close()
            connection.close()
            print("Connexion a la base de donnees fermee.")

# Fonction pour supprimer un utilisateur (à implémenter plus tard)
def delete_user():
    pass

# Fonction pour modifier un mot de passe (à implémenter plus tard)
def alter_password():
    pass

# Fonction pour ajouter une note (à implémenter plus tard)
def add_grade():
    pass

# Fonction pour supprimer une note (à implémenter plus tard)
def delete_grade():
    pass

# Fonction pour modifier une note (à implémenter plus tard)
def alter_grade():
    pass

# Fonction pour modifier la note maximale (à implémenter plus tard)
def alter_maximum_grade():
    pass

# Fonction pour modifier le coefficient d'une note (à implémenter plus tard)
def alter_coef():
    pass

# Fonction pour modifier les informations d'une note (à implémenter plus tard)
def alter_information_grade():
    pass

# Vérification de la connexion à la base de données lors de l'exécution du script
db_connection = connect_to_database()
if db_connection:
    db_connection.close()
    print("Connexion a la base de donnees fermee.")