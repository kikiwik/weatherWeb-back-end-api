# app/models.py
from sqlalchemy import Column, String, Enum, TIMESTAMP, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from enum import Enum as PyEnum
import random
import string
import uuid

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

class Token(Base):
    __tablename__ = "tokens"

    token = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())  # 使用 func.now() 作为默认值
    expires_at = Column(DateTime)

    user = relationship("User", back_populates="tokens")