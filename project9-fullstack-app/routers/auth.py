from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import  Users
from passlib.context import CryptContext
from database import SessionLocal
from starlette import  status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# create token variables
SECRET_KEY = '00cf6789e9cf6ecf780bf12b6117376ff91d8738c7008960481def44977d9bf8'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

class Token(BaseModel):
    access_token: str
    token_type: str


# FUNCTIONS

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="templates")

# pages

@router.get("/login-page")
def render_login_page(request:Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get("/register-page")
def render_register_page(request:Request):
    return templates.TemplateResponse('register.html', {'request': request})

# ##############END POINTS###################


# authenticate user
def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

# create access token
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# a function to decrypt the token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user.')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user( db: db_dependency, user: UserRequest):
    user_model = Users(
        email = user.email,
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        role = user.role,
        hashed_password = bcrypt_context.hash(user.password),
        is_active = True,
        phone_number = user.phone_number
    )

    db.add(user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):

    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user.')

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {"access_token": token, "token_type": 'bearer' }

