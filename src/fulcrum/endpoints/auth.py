import json
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from authlib.integrations.base_client import OAuthError
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from authlib.integrations.starlette_client import OAuth
import os
from fulcrum.config.auth import oauth
from fulcrum.db.user import User


router = APIRouter(prefix="/auth")
FULCRUM_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
SRC_DIR = os.path.join(FULCRUM_DIR, os.pardir)
ROOT_DIR = os.path.join(SRC_DIR, os.pardir)
CONFIG_FILE = os.path.abspath(os.path.join(os.path.abspath(ROOT_DIR), ".env"))
print("config_file:", CONFIG_FILE)

# Initialize our OAuth instance from the client ID and client secret specified in our .env file
config = Config(CONFIG_FILE)
oauth = OAuth(config)

print("config file values:", config.file_values)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get('/login/google', tags=['authentication'])  # Tag it as "authentication" for our docs
async def login(request: Request):
    if request.session.get("user") is None:
        # Redirect Google OAuth back to our application
        redirect_uri = request.url_for('auth_google')
        print("redirect_uri:", redirect_uri)
        return await oauth.google.authorize_redirect(request, redirect_uri)
    else:
        return {"email": request.session.get("user").get("email")}


@router.route('/auth/google', name="auth_google")
async def auth(request: Request):
    print("request.session:", json.dumps(request.session, indent=4))
    # Perform Google OAuth
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
    except OAuthError as e:
        return {"error": e.error}
    if user:
        request.session['user'] = dict(user)
        username = dict(user).get('email')
        userdb = User.objects(username=username)
        print("logged in")
        if not userdb:
            pass #TODO(dev): Create register page
    return JSONResponse({"email": user.get("email")})


@router.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/')
