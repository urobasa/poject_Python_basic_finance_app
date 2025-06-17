
def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "Username" in text

def test_successful_login(client):
    response = client.post("/login", data={"username": "testuser", "password": "1234"}, follow_redirects=True)
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "Logout" in text or "Категории" in text

def test_failed_login(client):
    response = client.post("/login", data={"username": "wrong", "password": "wrong"}, follow_redirects=True)
    text = response.get_data(as_text=True)
    assert "Invalid" in text or response.status_code == 401
