from fastapi import FastAPI, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.fulcrum.models.user import User

router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username + 'token'}


@router.route('/')
async def index(token: str = Depends(oauth2_scheme)):
    return {'token': token}


@router.post("/login", tags=["login_user"])
async def login(user) -> User:
    """
        Endpoint for logging in a user based on username and password. All passwords are hashed
        and salted when stored in MongoDB for compliance.

        req : {
            "username" : "Username of the user",
            "password" : "Password of the user"
        }
    """
    return {"response": "Hello World!!"}


@router.post("/logout", tags=["logout_user"])
async def logout(username):
    """
        Endpoint for logging out a user based on username.
    """
    return {"response": "Hello World!!"}
