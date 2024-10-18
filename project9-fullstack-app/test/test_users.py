from .utils import *
from routers.users import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert  response.json()['username'] == 'bravol'
    assert  response.json()['email'] == 'lumalabravo@gmail.com'
    assert  response.json()['first_name'] == 'Brian'
    assert  response.json()['last_name'] == 'Lumala'
    assert  response.json()['role'] == 'admin'
    assert  response.json()['phone_number'] == '1111111111'

def change_password_success(test_user):
    data = {
            "password":"testpassword",
            "new_password":"newpassword"
            }
    response = client.get("/users/password", json=data)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    # Providing an incorrect password to trigger the 401 Unauthorized error
    data = {
        "password": "wrongpassword",
        "new_password": "newpassword"
    }
    response = client.put("/users/password", json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}

def test_change_phone_number_success(test_user):
    response = client.put("/users/phone_number/999999")
    assert  response.status_code == status.HTTP_204_NO_CONTENT
