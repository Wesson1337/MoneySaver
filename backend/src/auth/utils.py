from datetime import timedelta, datetime
from typing import Optional

from jose import jwt

from backend.src.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM, pwd_context
from backend.src.auth.models import User


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def check_user_is_superuser(user: Optional[User]) -> bool:
    return user and user.is_superuser
