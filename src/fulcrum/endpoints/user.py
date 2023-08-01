import datetime
import json
from http.client import HTTPException
from typing import Annotated

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Form
from firebase_admin.auth import create_user
from firebase_admin.exceptions import FirebaseError
from mongoengine import *
from pydantic import EmailStr
from starlette.responses import JSONResponse

from fulcrum.config.auth import oauth
from fulcrum.endpoints.auth import get_token
from fulcrum.models.user import CreateUser
from fulcrum.db.user import User
user_router = APIRouter()

# from fulcrum.db.user import User

router = APIRouter(prefix="/api/users")


@router.get("/list", tags=["get_users"])
async def get_users():
    """
        Endpoint to get all users in the MongoDB collection. Used primarily for internal testing
        purposes.

    """
    return User.objects().to_json()


@router.get("/email/{email}", tags=["get_user"])
async def get_user_by_email(email: str):
    '''
        Endpoint to get user based on user's email
    '''
    users = json.loads(User.objects(email=email).to_json())
    return users[0] if users else None

# Note: currently Users are automatically created during the login process if they are not registered


@router.post("/register", tags=["register_user"])
async def register(userid: Annotated[str, Form()], email: Annotated[EmailStr, Form()], name: Annotated[str, Form()]) -> JSONResponse:
    """
        Endpoint for first time user registration.
    """
    User(userid=userid, email=email, name=name).save()
    user = User.objects(userid=userid)
    if user:
        print(json.loads(user[0].to_json()))
        user = json.loads(user[0].to_json())
        res = {"user": user}
    else:
        res = {"error": "Error creating user in database"}
    return JSONResponse(res)


