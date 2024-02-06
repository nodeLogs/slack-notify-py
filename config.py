from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self):
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_NAME')
        self.slack_token = os.getenv('SLACK_TOKEN')
        self.slack_channel = os.getenv('SLACK_CHANNEL')
