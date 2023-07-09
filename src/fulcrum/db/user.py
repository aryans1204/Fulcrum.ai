from mongoengine import Document, StringField, IntField, ReferenceField, ListField

from fulcrum.db.chatbot_config import Chatbot

class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    noChatbots = IntField(required=True, default=0)
    config = ListField(ReferenceField(Chatbot))



