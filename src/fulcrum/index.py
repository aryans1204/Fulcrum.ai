import firebase_admin
from authlib.integrations.starlette_client import OAuth
from firebase_admin import credentials
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
import os
import mongoengine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fulcrum.endpoints.chatbot_ops import router as chat_router
from fulcrum.endpoints.user import router as user_router
from fulcrum.endpoints.auth import router as auth_router
from fulcrum.endpoints.docs import router as docs_router
from fulcrum.endpoints.faq import router as faq_router
from fulcrum.auth.auth_jwt import JWTBearer

mongoengine.connect(host=os.environ["MONGODB_URL"])

# TODO: add frontend production url
origins = ["http://localhost:3000"]

config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        "scope": "openid email profile"
    }
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SECRET_KEY"],
)

routers = [auth_router, chat_router, user_router, docs_router, faq_router]
for router in routers:
    app.include_router(router)

cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
default_app = firebase_admin.initialize_app(cred)



@app.get("/")
async def main(request: Request):
    user = request.session.get('user')
    if not user:
        return {"message": "Hello Guest!!"}
    else:
        return {"message": f"Hello {user['name']}"}
