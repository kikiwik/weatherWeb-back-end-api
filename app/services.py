import random
import string
from dao import database

def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def save_verification_code(email: str, code: str):
    database.redis_client.setex(f"verification_code:{email}", 300, code)

def send_verification_code(email: str):
    verification_code = generate_verification_code()
    save_verification_code(email.email, verification_code)
    send_email(email.email, verification_code)
    return {"message": "Verification code sent"}