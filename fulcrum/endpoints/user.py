from fastapi import APIRouter
from mongoengine import *

router = APIRouter()

@router.get("/api/users", tags=["get_users"])
async def get_users():
    '''
        Endpoint to get all users in the MongoDB collection. Used primarily for internal testing
        purposes.

    '''
    return {"response": "Hello World!!"}

@router.post("/api/users", tags=["register_user"])
async def register(req):
    '''
        Endpoint for first time user registration. 

        req: {
            "username" : "Username of the user",
            "password" : "Password of the user"
        }
    '''
    return {"response": "Hello World!!"}

@router.post("/api/users/login", tags=["login_user"])
async def login(req):
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
async def logout(req):
    '''
        Endpoint for logging out a user based on username and password.

        req: {
            "username" : "User name of the user"
        }
    '''
    return {"response" : "Hello World!!"}


