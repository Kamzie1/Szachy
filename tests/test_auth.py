def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_register(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302