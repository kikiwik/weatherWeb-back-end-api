# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao import crud, database
from services import generate_verification_code, save_verification_code, send_email
from .. import dependencies
import schemas
router = APIRouter()



@router.post("/register", response_model=schemas.UserResponse)#注册用户
def register_user(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    dependencies.password_validator(user.password)
    verification_code = generate_verification_code()
    save_verification_code(user.email, verification_code)
    send_email(user.email, verification_code)
    if not dependencies.verify_verification_code(user.email, user.verification_code):
        raise HTTPException(status_code=400, detail="Incorrect or expired verification code")
    new_user = crud.create_user(db, user=user)
    token = crud.create_token(db, user_id=new_user.user_id)
    return {"user": new_user, "token": token.token}

@router.post("/login/password", response_model=schemas.UserResponse)
def login_user(user: schemas.UserLoginA, db: Session = Depends(database.SessionLocal)):
    # 在数据库中查找用户
    dependencies.password_validator(user.password)
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not dependencies.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = crud.create_token(db, user_id=db_user.user_id)
    return {"user": db_user, "token": token.token}

@router.post("/login/verification_code",response_model=schemas.UserResponse)
def login_user(user: schemas.UserloginB, db: Session = Depends(database.SessionLocal)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not Found")
    verification_code=generate_verification_code()
    save_verification_code(email,verification_code)
    send_email(email,verification_code)
    if not verify_verification_code(user.email,user.verification_code):
        raise HTTPException(status_code=400, detail="Incorrect or expired verification code")
    token = crud.create_token(db, user_id=db_user.id)
    return {"user": db_user, "token": token.token}