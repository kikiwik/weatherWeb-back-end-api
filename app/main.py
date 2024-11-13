# app/main.py
from fastapi import FastAPI
from .routers import users
from dao import crud, database
import uvicorn

app = FastAPI()


# 包含用户路由
app.include_router(users.router, prefix="/api/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=443, ssl_certfile="/path/to/certificate.crt", ssl_keyfile="/path/to/private.key")