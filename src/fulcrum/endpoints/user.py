import datetime
from typing import Annotated

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Form
from mongoengine import *
from starlette.responses import JSONResponse

from fulcrum.config.auth import oauth
from fulcrum.models.user import UserPublic, UserInDB
#from fulcrum.db.user import User

router = APIRouter(prefix="/api/users")


@router.get("/list", tags=["get_users"])
async def get_users() -> list[UserPublic]:
    """
        Endpoint to get all users in the MongoDB collection. Used primarily for internal testing
        purposes.

    """
    return [UserPublic()]


@router.post("/register", tags=["register_user"])
async def register(email: Annotated[str, Form()], name: Annotated[str, Form()]) -> JSONResponse:
    """
        Endpoint for first time user registration.
    """
    # TODO: generate id and check against ids in database, ensure no collision
    user = UserInDB(id="test", created_at=datetime.datetime.now(), updated_at=None, email=email, name=name)
    return JSONResponse({user: user})