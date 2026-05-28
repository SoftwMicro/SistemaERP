import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='pedidos',
                user='admin',
                password='010101',
                port=3306
            )
        except Error as e:
            raise Exception(f'Erro ao conectar ao banco de dados: {e}')

    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
