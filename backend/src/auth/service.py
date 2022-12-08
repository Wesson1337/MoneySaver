from datetime import timedelta, datetime
from typing import Optional

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.config import pwd_context, JWT_SECRET_KEY, JWT_ALGORITHM
from backend.src.auth.exceptions import NotSuperUserException
from backend.src.auth.models import User
from backend.src.auth.schemas import UserSchemaIn


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


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    user = await session.get(User, {"email": email})
    return user


async def authenticate_user(email: str, password: str, session: AsyncSession) -> Optional[User]:
    user = await get_user_by_email(email, session)
    if not user:
        return
    if not verify_password(password, user.hashed_password):
        return
    return user


async def create_user(current_user: User, new_user_data: UserSchemaIn, session: AsyncSession) -> User:
    if new_user_data.is_superuser and not check_user_is_superuser(current_user):
        raise NotSuperUserException()

    new_user_dict = _change_user_password_to_hashed_password(new_user_data)
    new_user = User(**new_user_dict)
    session.add(new_user)
    await session.commit()

    return new_user


def _change_user_password_to_hashed_password(user_data: UserSchemaIn) -> dict:
    user_dict = user_data.dict()
    hashed_password = get_password_hash(user_data.password1)
    del user_dict['password1']
    del user_dict['password2']
    user_dict.update({'hashed_password': hashed_password})
    return user_dict
