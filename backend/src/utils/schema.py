from pydantic import BaseModel


class BaseORMSchema(BaseModel):
    class Config:
        orm_mode = True
