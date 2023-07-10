from fastapi import APIRouter
from mongoengine import *
from ...fulcrum.models.user import User


router = APIRouter(prefix="/api/users")


@router.get("/list", tags=["get_users"])
async def get_users() -> list[User]:
    """
        Endpoint to get all users in the MongoDB collection. Used primarily for internal testing
        purposes.

    """
    return [User()]


@router.post("/register", tags=["register_user"])
async def register(user) -> User:
    """
        Endpoint for first time user registration.

        req: {
            "username" : "Username of the user",
            "password" : "Password of the user"
        }
    """
    return {"response": "Hello World!!"}


