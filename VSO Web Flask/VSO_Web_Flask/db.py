#Model

import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jyfkf596f!BYFZEHf58f65zf!",
            database="users"
        )

        if connection.is_connected():
            print("Connexion reussie a la base de donnees 'users'.")
            return connection
    except Error as e:
        print(f"Erreur lors de la connexion a la base de donnees : {e}")
        return None

db_connection = connect_to_database()
if db_connection:
    db_connection.close()
    print("Connexion a la base de donnees fermee.")