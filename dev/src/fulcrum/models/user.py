from pydantic import BaseModel
from src.fulcrum.models.chatbot import Chatbot


class User(BaseModel):
    username: str
    password: str
    noChatbots: int
    config: list[Chatbot]



