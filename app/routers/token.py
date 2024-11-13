from fastapi import APIRouter, Depends
from .. import schemas
from dependencies import get_current_user
router = APIRouter()

@router.get("/protected-route", response_model=schemas.UserResponse)
def protected_route(current_user: schemas.User = Depends(get_current_user)):
    return current_user
