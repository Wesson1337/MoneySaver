from typing import Optional

from pydantic import EmailStr, constr, validator, BaseModel

from backend.src.utils.schema import BaseORMSchema


class UserSchemaIn(BaseORMSchema):
    email: EmailStr
    password1: constr(min_length=6, max_length=32)
    password2: constr(min_length=6, max_length=32)
    is_superuser: bool = False

    @validator('password2')
    def password_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError("passwords doesn't match")


class UserSchemaPatch(BaseORMSchema):
    email: Optional[EmailStr]
    password: Optional[constr(min_length=6, max_length=32)]
    is_active: Optional[bool]
    is_superuser: Optional[bool]


class UserSchemaOut(BaseORMSchema):
    id: int
    email: str
    is_active: bool
    is_superuser: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
