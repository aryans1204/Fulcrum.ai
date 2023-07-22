from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter
from mongoengine import *
from ...fulcrum.models.user import User

<<<<<<< Updated upstream
=======
from fulcrum.config.auth import oauth
from fulcrum.db.user import User
>>>>>>> Stashed changes

router = APIRouter(prefix="/api/users")


<<<<<<< Updated upstream
@router.get("/list", tags=["get_users"])
async def get_users() -> list[User]:
    """
=======
@router.get("/", tags=["get_users"])
async def get_users():
    '''
>>>>>>> Stashed changes
        Endpoint to get all users in the MongoDB collection. Used primarily for internal testing
        purposes.

    """
    return [User()]

<<<<<<< Updated upstream

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

=======
>>>>>>> Stashed changes

@router.get("/register", tags=["register"])
async def register():
    """
        Endpoint to register user
    """
    return
