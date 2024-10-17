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