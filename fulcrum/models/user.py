from mongoengine import Document, StringField, IntField

class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    noChatbots = IntField(required=True, default=0)


