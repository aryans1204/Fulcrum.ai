from mongoengine import StringField, IntField, Document

class Chatbot(Document):
    chatbot_id = StringField(required=True)
    chromadb_index = StringField(required=True)
    gcs_bucket = StringField(required=True)

