from pydantic import BaseModel, HttpUrl

class Chatbot(BaseModel):
    chatbot_id = str
    gcs_bucket = HttpUrl

class TrainingModel(BaseModel):
    username: str
    chatbot_id: str
