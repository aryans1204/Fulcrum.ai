import os

import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials

from src.chatbot.endpoints.comms import router as chat_router
from src.chatbot.endpoints.auth import router as auth_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(auth_router)

cred = credentials.Certificate(os.environ["FIREBASE_CREDENTIALS"])
default_app = firebase_admin.initialize_app(cred)

@app.get("/")
async def main():
    return {"message":"Hello World"}

