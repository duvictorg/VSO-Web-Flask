import mysql.connector
import os
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from dotenv import load_dotenv

load_dotenv()
fernet_key = os.getenv('fernet_key',default = '')
fernet = Fernet(fernet_key)
# Fixed key and IV
FIXED_KEY = os.getenv('fixed_key_aes',default = '').encode()  # 256-bit key (32 bytes)
FIXED_IV = os.getenv('fixed_iv_aes',default = '').encode()  # 128-bit IV (16 bytes)

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
            user='pronote',
            password=os.getenv('mysql_password_ecole',default = ''),
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