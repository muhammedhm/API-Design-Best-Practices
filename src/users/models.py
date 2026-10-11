from sqlalchemy import Column, Integer, String, Text,Boolean
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(100))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    mobile_number = Column(String(15), nullable=True)
    