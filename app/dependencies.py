from fastapi import Depends, HTTPException, status
from dao import database,crud
from sqlalchemy.orm import Session
import bcrypt
import re

PASSWORD_REGEX = re.compile(r"^[a-zA-Z0-9@#$%^&+=]{8,}$")



def get_current_user(token: str, db: Session = Depends(database.SessionLocal)):
    db_token = crud.get_user_by_token(db, token)
    if not db_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return db_token.user

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def password_validator(password: str):
    if not PASSWORD_REGEX.match(password):
         raise HTTPException(
            status_code=400, 
            detail="Password must contain only allowed characters and be at least 8 characters long."
        )
