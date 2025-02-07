import mysql.connector
from cryptography.fernet import Fernet

fernet = Fernet('wOqAcmjUsZmRBCqMuC-SasMhBGxmnGhpk9yYTh9n9DA=')

def encrypt_data(data):
    return fernet.encrypt(data.encode()).decode() if type(data) != bytes else fernet.encrypt(data).decode()

def decrypt_data(data):
    return fernet.decrypt(data.encode()).decode() if type(data) != bytes else fernet.decrypt(data).decode()

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Jyfkf596f!BYFZEHf58f65zf!',
            database='ecole'
                                                                                                                      
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def query(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def execute(self, query, values=None):
        self.cursor.execute(query, values)
        self.connection.commit()
    
    def close(self):
        self.cursor.close()