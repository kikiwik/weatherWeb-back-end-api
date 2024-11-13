# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)