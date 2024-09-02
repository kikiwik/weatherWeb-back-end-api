# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database, security
from services import generate_verification_code, save_verification_code, send_email
from dependencies import verify_verification_code
router = APIRouter()

@router.post("/register/send-code")
def send_registration_code(email: schemas.EmailStr, db: Session = Depends(database.SessionLocal)):
    existing_user = crud.get_user_by_email(db, email=email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    verification_code = generate_verification_code()
    save_verification_code(email, verification_code)
    send_email(email, verification_code)
    
    return {"message": "Verification code sent"}

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    if not verify_verification_code(user.email, user.verification_code):
        raise HTTPException(status_code=400, detail="Incorrect or expired verification code")

    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = crud.create_user(db, user=user)
    return new_user 

@router.post("/login/password", response_model=schemas.UserResponse)
def login_user(user: schemas.UserLoginA, db: Session = Depends(database.SessionLocal)):
    # 在数据库中查找用户
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not security.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    return db_user

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
    return db_user