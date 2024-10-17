from routers.auth import get_current_user
from routers.todos import get_db
from fastapi import status
from .utils import *


#overriding the original db, and current user
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()[0]
    assert data['title'] == 'Learn to code!'
    assert data['description'] == 'Need to learn everyday'
    assert data['priority'] == 5
    assert data['complete'] == False
    assert data['owner_id'] == 1
    assert data['id'] == 1
    # OR
    assert response.json()  == [{'title':'Learn to code!','description':'Need to learn everyday','priority':5,'complete':False,'owner_id':1, 'id': 1}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()  == {'title':'Learn to code!','description':'Need to learn everyday',
                                 'priority':5,'complete':False,'owner_id':1, 'id': 1}

def test_read_one_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() =={'detail': 'Todo not found'}



def test_create_todo(test_todo):
    requested_data={
        'title': 'New Todo!',
        'description': 'New todo description',
        'priority':5,
        "complete": False
    }

    response = client.post('/todo/', json=requested_data)
    assert response.status_code == 201

    db =TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()

    assert model.title == requested_data.get('title')
    assert model.description == requested_data.get('description')
    assert model.priority == requested_data.get('priority')
    assert model.complete == requested_data.get('complete')

def test_update_todo(test_todo):
    request_data = {
        'title':'Change the title of the todo already saved!',
        'description':'Need to learn everyday!',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todo/1", json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert  model.title == 'Change the title of the todo already saved!'



def test_update_todo_not_found(test_todo):
    request_data = {
        'title':'Change the title of the todo already saved!',
        'description':'Need to learn everyday!',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json()  == {'detail': 'Todo not found.'}


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert  model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert  response.json() == {'detail': 'Todo not found.'}
