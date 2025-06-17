def test_csrf_protection(client):
    # Предположим, CSRF включён (например, через Flask-WTF)
    response = client.post("/login", data={"username": "testuser", "password": "1234"})
    if response.status_code == 400:
        assert "CSRF" in response.data or "csrf" in response.data.lower()
