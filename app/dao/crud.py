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
    #删除旧token
    db_user = models.User(email=user.email, password=hashed_password.decode('utf-8'),user_id=str(uuid.uuid4())[:8])
    #插入新token
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_token(db: Session, user_id: str):
    token = models.Token(user_id=user_id,permissions=models.UserStatus.NEW, expires_at=datetime.now(timezone.utc) + timedelta(days=1))
    db.add(token)
    db.commit()
    db.refresh(token)
    return {
        "token":token.token,
        "permissions":token.permissions,
        "expires_at":token.created_at.isoformat()
    }


    
def get_user_permission(db:Session,user_id:str):
    db_user=db.query(models.User).filter(models.User.user_id==user_id).first()
    permissions=db_user.status
    return permissions


def create_or_update_token(db:Session,user_id:str):
    exist_token=db.query(models.Token).filter(models.Token.user_id==user_id,models.Token.expires_at>datetime.now(timezone.utc)).first()
    if exist_token :
        return {
        "token":exist_token.token,
        "permissions":exist_token.permissions,
        "expires_at":exist_token.expires_at.isoformat()
    }
    else:
        new_token=models.Token(user_id=user_id,permissions=get_user_permission(db,user_id), expires_at=datetime.now(timezone.utc) + timedelta(days=1))
        db.query(models.Token).filter(models.Token.user_id==user_id).delete()
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        return {
            "token":new_token.token,
            "permissions":new_token.permissions,
            "expires_at":new_token.expires_at.isoformat()
        }
    