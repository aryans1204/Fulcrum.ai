import string
from typing import Optional

from bson import ObjectId
from pydantic import EmailStr
from fulcrum.models.core import DateTimeModelMixin, IDModelMixin, CoreModel


class UserCreateBase(CoreModel):
    email: EmailStr
    name: str
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False
    no_chatbots: int = 0
    chatbot_configs: list = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "name": "Jane Doe",
                "email_verified": True,
                "is_active": True,
                "is_superuser": False,
                "no_chatbots": 0,
                "chatbots": []
            }
        }


class UserUpdateBase(CoreModel):
    email: Optional[EmailStr]
    name: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "name": "Jane Doe",
                "email_verified": True,
                "is_active": True,
                "is_superuser": False,
                "no_chatbots": 0,
                "chatbots": []
            }
        }


class CreateUser(IDModelMixin, UserCreateBase, DateTimeModelMixin):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """


class UpdateUser(DateTimeModelMixin, UserUpdateBase):
    pass
