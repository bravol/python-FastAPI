from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import  Users
from passlib.context import CryptContext
from database import SessionLocal
from starlette import  status
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# FUNCTIONS
# authenticate user
def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user( db: db_dependency, user: UserRequest):
    user_model = Users(
        email = user.email,
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        role = user.role,
        hashed_password = bcrypt_context.hash(user.password),
        is_active = True
    )

    db.add(user_model)
    db.commit()

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):

    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        return 'Failed Authentication'
    return 'Successful authentication'