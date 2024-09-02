from fastapi import Depends, HTTPException
from database import redis_client

def verify_verification_code(email: str, code: str):
    stored_code = redis_client.get(f"verification_code:{email}")
    if stored_code and stored_code == code:
        redis_client.delete(f"verification_code:{email}")
        return True
    return False