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


CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def get_registration(request: Request):
    registered = False
    user = request.session.get("user")
    email = dict(user).get('email')
    request.session["email"] = email
    users = User.objects()
    _id = None
    if users:
        userdb = User.objects(email=email)
        print(userdb)
        print(type(userdb))
        if userdb:
            userdb = json.loads(userdb.to_json())[0]
            print(userdb)
            registered = True
            _id = userdb["_id"]['$oid']
            request.session["userid"] = _id

            print("_id", _id)
    return JSONResponse({"email": email, "id": _id, "registered": registered})


@router.get('/login/google', tags=['authentication'])  # Tag it as "authentication" for our docs
async def login(request: Request):
    if request.session.get("user") is None:
        # Redirect Google OAuth back to our application
        redirect_uri = request.url_for('auth_google')
        print("redirect_uri:", redirect_uri)
        return await oauth.google.authorize_redirect(request, redirect_uri)
    else:
        return get_registration(request)


@router.route('/auth/google', name="auth_google")
async def auth(request: Request):
    print("request.session:", json.dumps(request.session, indent=4))
    registered = False
    # Perform Google OAuth
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        request.session["user"] = user
    except OAuthError as e:
        return {"error": e.error}

    return get_registration(request)


@router.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)
    request.session.pop('email', None)
    request.session.pop('userid', None)

    return RedirectResponse(url='/')
