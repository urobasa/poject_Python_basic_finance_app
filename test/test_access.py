from app.extensions import db

def test_user_cannot_access_others_data(app, client):
    with app.app_context():
        from app.models.user import User
        from app.models.account import Account
        u2 = User(username="hacker", password_hash="x")
        db.session.add(u2)
        db.session.commit()
        acc = Account(name="Secret", type="card", user_id=u2.id)
        db.session.add(acc)
        db.session.commit()
        acc_id = acc.id

    client.post("/login", data={"username": "testuser", "password": "1234"})
    response = client.get(f"/accounts/{acc_id}")
    assert response.status_code in [403, 404]
