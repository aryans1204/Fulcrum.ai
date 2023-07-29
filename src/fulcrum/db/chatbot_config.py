import datetime

from mongoengine import StringField, Document, URLField, DateTimeField


class Chatbot(Document):
    chatbot_id = StringField(required=True)
    chromadb_index = StringField(required=True)
    gcs_bucket = StringField(required=True)
    deployedURL = URLField(required=True)
    personality = StringField(required=True)
    dataFileName = StringField(required=True)
    created_date = DateTimeField(default=datetime.datetime.now())
    updated_date = DateTimeField(default=datetime.datetime.now())

