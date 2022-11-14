from sqlalchemy import Column

from ..database import Base


class Income(Base):
    name = Column()