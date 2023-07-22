import os

import mongoengine
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from fulcrum.endpoints.chatbot_ops import router as chat_router
from fulcrum.endpoints.user import router as user_router
from fulcrum.endpoints.auth import router as auth_router

routers = [chat_router, user_router, auth_router]

mongoengine.connect(host=os.environ["MONGODB_URL"])

app = FastAPI()
for router in routers:
    app.include_router(router)

app.add_middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"])


@app.get("/")
async def main():
    return {"message": "Hello World!!"}
