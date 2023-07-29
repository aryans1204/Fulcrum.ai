import json
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from authlib.integrations.base_client import OAuthError
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from fulcrum.auth.auth_jwt import create_access_token, jsonify_jwt

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


CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def get_token(user: dict):
    registered = False
    email = dict(user).get('email')
    users = User.objects()
    _id = None
    name = None
    if users:
        userdb = User.objects(email=email)
        print(userdb)
        print(type(userdb))
        if userdb:
            userdb = json.loads(userdb.to_json())[0]
            print(userdb)
            registered = True
            _id = userdb["_id"]['$oid']
            name = userdb["name"]
            print("_id", _id)
    data = {"email": email, "id": _id, "name": name, "registered": registered}
    return JSONResponse(jsonify_jwt(create_access_token(data=data)))


@router.get('/login/google', tags=['authentication'])  # Tag it as "authentication" for our docs
async def login(request: Request):
    if request.session.get("user") is None:
        # Redirect Google OAuth back to our application
        redirect_uri = request.url_for('auth_google')
        print("redirect_uri:", redirect_uri)
        return await oauth.google.authorize_redirect(request, redirect_uri)
    else:
        return RedirectResponse("/")


@router.route('/auth/google', name="auth_google")
async def auth(request: Request):
    print("request.session:", json.dumps(request.session, indent=4))
    registered = False
    # Perform Google OAuth
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
    except OAuthError as e:
        print("oauth_error:", e)
        print("clientID:", os.environ.get('GOOGLE_CLIENT_ID'))
        print("clientSecret:", os.environ.get('GOOGLE_CLIENT_SECRET'))
        raise HTTPException(status_code=500, detail=str(e))
    print("testing...")
    return get_token(user)


@router.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)
    request.session.pop('email', None)
    request.session.pop('userid', None)

    return RedirectResponse(url='/')
