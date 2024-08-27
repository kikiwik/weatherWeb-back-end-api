# app/models.py
from sqlalchemy import Column, String, Enum, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
import random
import string

Base = declarative_base()

class UserStatus(PyEnum):
    BANNED = "banned"
    NEW = "new"
    BELIEVABLE = "believable"
    AD = "AD"

def generate_uuid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(String(8), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.NEW, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")
