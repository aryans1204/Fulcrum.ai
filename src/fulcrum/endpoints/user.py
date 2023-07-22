from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter
from mongoengine import *
from fulcrum.config.auth import oauth
from fulcrum.models.user import UserPublic
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
async def register(user) -> UserPublic:
    """
        Endpoint for first time user registration.

        req: {
            "username" : "Username of the user",
            "password" : "Password of the user"
        }
    """
    return {"response": "Hello World!!"}