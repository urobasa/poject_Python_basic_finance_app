import pytest
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        # Добавим тестового пользователя
        user = User(username="testuser", password_hash=generate_password_hash("1234"))
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    client.post("/login", data={"username": "testuser", "password": "1234"})
    return client
