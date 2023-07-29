from fastapi import FastAPI
from src.chatbot.endpoints.comms import router

app = FastAPI()

app.include_router(router)

@app.get("/")
async def main():
    return {"message":"Hello World"}

