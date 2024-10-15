from fastapi import APIRouter
from pydantic import BaseModel
from models import  Users
from passlib.context import CryptContext


router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth")
async def create_user(user: UserRequest):
    user_model = Users(
        email = user.email,
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        role = user.role,
        hashed_password = bcrypt_context.hash(user.password),
        is_active = True
    )

    return user_model
