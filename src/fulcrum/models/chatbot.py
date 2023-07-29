from pydantic import BaseModel, HttpUrl


class Chatbot(BaseModel):
    vertex_url = HttpUrl
    chatbot_id = str
    vertex_bucket = HttpUrl
    gcs_bucket = HttpUrl


class TrainingModel(BaseModel):
    username: str
    password: str