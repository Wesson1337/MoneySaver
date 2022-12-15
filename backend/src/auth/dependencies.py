from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM
from backend.src.auth.exceptions import CredentialsException, InactiveUserException
from backend.src.auth.models import User
from backend.src.auth.schemas import TokenData
from backend.src.auth.service import get_user_by_email
from backend.src.config import DEFAULT_API_PREFIX
from backend.src.dependencies import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{DEFAULT_API_PREFIX}/token")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           session: AsyncSession = Depends(get_async_session)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise CredentialsException()
        token_data = TokenData(email=email)
    except (JWTError, ValidationError):
        raise CredentialsException()

    user = await get_user_by_email(token_data.email, session)
    if user is None:
        raise CredentialsException()
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user

