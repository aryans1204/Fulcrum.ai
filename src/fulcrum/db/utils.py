import json

from bson import ObjectId

from fulcrum.db.user import User


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


def get_user_by_id(_id, _dict=True):
    user = User.objects.get(userid=_id)
    if not _dict:
        return user
    else:
        return user_to_dict(user)


def user_to_dict(user):
    return json.loads(user.to_json())
