from sqlalchemy import Column, Boolean, Integer

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id_ = Column(Integer, primary_key=True)
    discount = Column(Boolean, default=False)
