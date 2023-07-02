from fastapi import APIRouter
from mongoengine import *
from ../models/user import User, LoginUser, SignUpUser


router = APIRouter()

@router.get("/api/users", tags=["get_users"])
async def get_users() -> list[User]:
    '''
        Endpoint to get all users in the MongoDB collection. Used primarily for internal testing
        purposes.

    '''
    return {"response": "Hello World!!"}

@router.post("/api/users", tags=["register_user"])
async def register(user: SignUpuser) -> User:
    '''
        Endpoint for first time user registration. 

        req: {
            "username" : "Username of the user",
            "password" : "Password of the user"
        }
    '''
    return {"response": "Hello World!!"}

@router.post("/api/users/login", tags=["login_user"])
async def login(user: LoginUser) -> User:
    '''
        Endpoint for logging in a user based on username and password. All passwords are hashed
        and salted when stored in MongoDB for compliance.

        req : {
            "username" : "User name of the user",
            "password" : "Password of the user"
        }
    '''
    return {"response": "Hello World!!"}

@router.post("/api/users/logout", tags=["logout_user"])
async def logout(username):
    '''
        Endpoint for logging out a user based on username and password.
    '''
    return {"response" : "Hello World!!"}


