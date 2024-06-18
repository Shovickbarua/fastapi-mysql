from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(255))
    description = Column(String(255))
    user_id = Column(Integer)
