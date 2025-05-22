# backend/tests/utils/user.py
from typing import Dict
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import random
import string

from app.core.config import settings
from app.schemas.user import UserCreate
from app.crud import user as crud_user
from app.db.models.user import User as UserModel 

def random_lower_string(length: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))

def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string(6)}.com"

def create_random_user(db: Session, is_superuser: bool = False, is_active: bool = True) -> UserModel:
    email = random_email()
    password = random_lower_string(8)
    full_name = random_lower_string(10)
    user_in = UserCreate(email=email, password=password, full_name=full_name, is_superuser=is_superuser, is_active=is_active)
    user_obj = crud_user.create_user(db=db, user=user_in) 
    return user_obj

def authentication_token_from_email(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

