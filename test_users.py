from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

token: str

def test_register_success():
    user = {
        "firstname": "Tue",
        "lastname": "Hellstern",
        "email": "testlogin@mail.com",
        "phonenumber": "2123222",
        "loc_id": 2200,
        "address": "Guldbergsgade 29N",
        "password": "1234Tecc1"
    }
    response = client.post("/users/register", json=user)
    assert response.status_code == 201

def test_login_success():
    user = {
        "email": "testlogin@mail.com",
        "password": "1234Tecc1"
    }   
    response = client.post("/users/login", json=user)
    assert 'success' in response.json()
    assert response.status_code == 200
    
def test_login_user_not_found():
    user = {
        "email": "testlogindoesnotexist@mail.com",
        "password": "12"
    }   
    response = client.post("/users/login", json=user)
    assert 'error' in response.json()
    assert response.status_code == 404

def test_login_password_incorrect():
    user = {
        "email": "testlogin@mail.com",
        "password": "1"
    }   
    response = client.post("/users/login", json=user)
    assert 'error' in response.json()
    assert response.status_code == 401


def test_user_delete_unauthorized():
    user = {
        "email": "testlogin@mail.com",
        "password": "1"
    }   
    response = client.delete("/users/delete", json=user)
    #token = response.json()['token']['access_token']
    assert response.status_code == 401

def test_user_delete_authorized():
    user = {
        "email": "testlogin@mail.com",
        "password": "1234Tecc1"
    }   
    response = client.post("/users/login", json=user)
    token = response.json()['token']['access_token']
    user = {
        "email": "testlogin@mail.com"
    }
    response = client.delete("/users/delete", json=user, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200