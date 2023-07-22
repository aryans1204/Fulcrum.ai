from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
import os
import mongoengine
from fastapi import FastAPI
from fulcrum.endpoints.chatbot_ops import router as chat_router
from fulcrum.endpoints.user import router as user_router
from fulcrum.endpoints.auth import router as auth_router

mongoengine.connect(host=os.environ["MONGODB_URL"])

config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        "scope":"openid email profile"
    }
)

routers = [auth_router, chat_router, user_router]

app = FastAPI()
for router in routers:
    app.include_router(router)

app.add_middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"])

@app.get("/")
async def main():
    return {"message": "Hello World!!"}


