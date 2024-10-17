from sqlalchemy import create_engine, StaticPool,text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from routers.auth import get_current_user
from routers.todos import get_db
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todos

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,

)

TestingSessionLocal =  sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'bravol', 'id':1, 'user_role': 'admin'}

#overriding the original db, and current user
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        id = 1,
        title='Learn to code!',
        description='Need to learn everyday',
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()

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



