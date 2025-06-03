import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key-default')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://finance_user:finance_pass@db:5432/finance_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
