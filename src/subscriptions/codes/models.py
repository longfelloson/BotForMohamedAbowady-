from sqlalchemy import Column, Integer

from src.database import Base


class Code(Base):
    __tablename__ = 'codes'

    id_ = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer, unique=True)
