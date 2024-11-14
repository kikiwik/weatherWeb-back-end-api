# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao import crud, database
import services
from .. import dependencies
import schemas
import asyncio
router = APIRouter()



@router.post("/register", response_model=schemas.UserResponse)#注册用户
def register_user(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    dependencies.password_validator(user.password)
    code=services.create_verification_code(email=user.email)
    asyncio.create_task(services.delete_expired_codes())
    ret = services.send_verification_code(code=code,email=user.email)
    if ret :
        print("验证码发送成功")
    else:
        print("验证码发送失败")
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
async def login_user(user:schemas.UserloginB,db: Session = Depends(database.SessionLocal)):
    #查找用户
    db_user = crud.get_user_by_email(db,email=user.email)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found !")
    code=services.create_verification_code(email=db_user.email)
    asyncio.create_task(services.delete_expired_codes())
    ret = services.send_verification_code(code=code,email=db_user.email)
    if ret :
        print("验证码发送成功")
    else:
        print("验证码发送失败")

    if services.verify_verification_code(code=user.verification_code,email=db_user.email):
        return {"user":db_user}
    else:
        raise HTTPException(status_code=401,detail="Verification code is incorrect or has expired.")
        

