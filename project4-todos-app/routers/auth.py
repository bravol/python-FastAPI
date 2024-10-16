from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends
from jose.constants import ALGORITHMS
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import  Users
from passlib.context import CryptContext
from database import SessionLocal
from starlette import  status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt



router = APIRouter()

SECRET_KEY = '00cf6789e9cf6ecf780bf12b6117376ff91d8738c7008960481def44977d9bf8'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str


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
    return user

# create access token
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


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

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):

    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        return 'Failed Authentication'

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": 'bearer' }
