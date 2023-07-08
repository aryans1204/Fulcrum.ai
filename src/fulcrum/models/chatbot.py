from pydantic import BaseModel, HttpUrl

class Chatbot(BaseModel):
    chatbot_id = str
    gcs_bucket = HttpUrl
    chromadb_index = str

class TrainingModel(BaseModel):
    username: str
    chatbot_id: str
