import mysql.connector


class Database:
    def __init__(self,config):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='pronote',
            password='pronote',
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