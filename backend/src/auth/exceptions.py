from fastapi import HTTPException
from starlette import status


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={'WWW-Authenticate': "Bearer"}
        )


class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )


class IncorrectEmailOrPasswordException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )


class EmailAlreadyExistsException(HTTPException):
    def __init__(self, email):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {email} already exists"
        )


class UserNotFoundException(HTTPException):
    def __init__(self, user_id):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} is not found"
        )
