import mysql.connector
from mysql.connector import Error

class DBConnector:
    def __init__(self, config):
        self.config = config

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.config.db_host,
                port=self.config.db_port,
                user=self.config.db_user,
                password=self.config.db_password,
                database=self.config.db_name
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def get_risk_transactions(self, last_processed_id=0):
        connection = self.connect()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT * FROM core.project_transactions 
                WHERE status = 'risk_processing' AND id > %s
                ORDER BY id ASC  # Сортировка по возрастанию id
            """
            cursor.execute(query, (last_processed_id,))
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            connection.close()


    def get_project_name(self, project_id):
        connection = self.connect()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT name FROM core.projects WHERE id = %s"
            cursor.execute(query, (project_id,))
            result = cursor.fetchone()
            return result['name'] if result else None
        finally:
            cursor.close()
            connection.close()

    def get_transaction_id(self, hash_transaction):
        connection = self.connect()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT id FROM core.transaction_approvements WHERE hash_transaction = %s"
            cursor.execute(query, (hash_transaction,))
            result = cursor.fetchone()
            return result['id'] if result else None
        finally:
            cursor.close()
            connection.close()
