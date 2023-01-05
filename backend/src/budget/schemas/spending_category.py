from pydantic import conint, constr

from backend.src.utils import BaseORMSchema


class SpendingCategorySchemaOut(BaseORMSchema):
    id: conint(ge=1)
    name: constr(max_length=255)
