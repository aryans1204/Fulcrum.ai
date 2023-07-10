import uvicorn
from fastapi import FastAPI
from src.chatbot.endpoints.comms import router as chatbot_comms_router
from src.fulcrum.endpoints.auth import router as auth_router
from src.fulcrum.endpoints.chatbot_ops import router as chatbot_ops_router
from src.fulcrum.endpoints.user import router as user_router

app = FastAPI()

routers = [chatbot_comms_router, auth_router, chatbot_ops_router, user_router]
for router in routers:
    app.include_router(router)


@app.get("/")
async def main():
    return {"message": "Hello World!!"}


if __name__ == "__main__":
    uvicorn.run(app)
