def test_operations_filtering(auth_client, follow_redirects=True):
    # Предположим, фильтрация по дате/категории через query-параметры
    response = auth_client.get("/operations?category=1", follow_redirects=True)
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "Операции" in text
