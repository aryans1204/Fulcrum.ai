from pydantic import BaseModel
from chatbot import Chatbot

class User(BaseModel):
    username: str
    password: str
    noChatbots: int
    config: list[Chatbot]


class LoginUser(BaseModel):
    username: str
    password: str


class SignUpUser(BaseModel):
    username: str
    password: str

