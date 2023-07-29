import datetime

from mongoengine import Document, StringField, IntField, ReferenceField, ListField, DateTimeField, ObjectIdField, EmailField, BooleanField
from bson import ObjectId


class Question(Document):
    questionID = ObjectIdField(default=ObjectId, primary_key=True)
    email = EmailField(required=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.now())
