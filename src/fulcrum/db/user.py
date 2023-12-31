import datetime

from mongoengine import Document, StringField, IntField, ReferenceField, ListField, DateTimeField, ObjectIdField, \
    EmailField, BooleanField, PULL
from bson import ObjectId

from fulcrum.db.chatbot_config import Chatbot


class User(Document):
    userid = StringField(required=True, primary_key=True)
    email = EmailField(required=True)
    name = StringField(required=True)
    email_verified = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)
    no_chatbots = IntField(default=0)
    chatbotConfigs = ListField(ReferenceField(Chatbot, reverse_delete_rule=PULL), default=[])
    created_date = DateTimeField(required=True, default=datetime.datetime.now())
    updated_date = DateTimeField(default=datetime.datetime.now())



