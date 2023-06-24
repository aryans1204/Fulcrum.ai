from mongoegine import StringField, IntField, Document

class Chatbot(Document):
    vertex_url = StringField(required=True)
    chatbot_id = StringField(required=True)
    vertex_bucket = StringField(required=True)
    gcs_bucket = StringField(required=True)

