import mysql.connector
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

fernet = Fernet('wOqAcmjUsZmRBCqMuC-SasMhBGxmnGhpk9yYTh9n9DA=')
# Fixed key and IV
FIXED_KEY = b'c0156eb3b5294d0b320aab84'  # 256-bit key (32 bytes)
FIXED_IV = b'0b12a385c74ca5ca'  # 128-bit IV (16 bytes)

def encrypt_username(plaintext):
    cipher = AES.new(FIXED_KEY, AES.MODE_CBC, FIXED_IV)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(ciphertext)

def decrypt_username(ciphertext):
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(FIXED_KEY, AES.MODE_CBC, FIXED_IV)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

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