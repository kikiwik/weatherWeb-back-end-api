# app/crud.py
from sqlalchemy.orm import Session
from . import models
from ..schemas import UserCreate
import bcrypt
from datetime import datetime, timezone, timedelta
import uuid

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(email=user.email, password=hashed_password.decode('utf-8'),user_id=str(uuid.uuid4())[:8])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_token(db: Session, user_id: str):
    token = models.Token(user_id=user_id, expires_at=datetime.now(timezone.utc) + timedelta(days=1))
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def get_user_by_token(db: Session, token: str):
    return db.query(models.Token).filter(
        models.Token.token == token, 
        models.Token.expires_at > datetime.now(timezone.utc)
    ).first()