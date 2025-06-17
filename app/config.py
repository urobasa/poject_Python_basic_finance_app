import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key-default')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://finance_user:finance_pass@db:5432/finance_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"

class ProdConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False  # Отключаем CSRF для обычных тестов
    SECRET_KEY = "testkey"
