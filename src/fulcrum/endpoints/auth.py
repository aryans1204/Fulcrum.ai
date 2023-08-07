import json
import warnings
from typing import Optional, List, Annotated
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from authlib.integrations.base_client import OAuthError
from fastapi.params import Form
from firebase_admin.app_check import verify_token
from firebase_admin.auth import get_user, UserNotFoundError, create_user, verify_id_token, InvalidIdTokenError, \
    ExpiredIdTokenError, RevokedIdTokenError, CertificateFetchError, UserDisabledError
from firebase_admin.exceptions import FirebaseError
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
#print("config_file:", CONFIG_FILE)

# TODO: Add Client production base url
CLIENT_BASE_URL = 'http://localhost:3000/' if os.environ.get(
    "ENV", "development") == 'development' else ''
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.post("/jwt-token/get")
def get_token(access_token: str, user: dict):
    warnings.warn("Deprecated in favor of a simpler way")
    registered = False
    _id = None
    name = None
    email = user.get('email')
    if email:
        users = User.objects()
        if users:
            userdb = User.objects(email=email)
            #print(userdb)
            #print(type(userdb))
            if userdb:
                userdb = json.loads(userdb.to_json())[0]
                #print(userdb)
                registered = True
                _id = userdb["_id"]['$oid']
                name = userdb["name"]
                #print("_id", _id)

    data = {"email": email, "id": _id, "gcip_token": access_token, "user": user, "name": name, "registered": registered}

    return jsonify_jwt(create_access_token(data=data))


@router.post("/verify/firebase-token")
def verify_firebase_token(token: Annotated[str, Form()]):
    try:
        return verify_token(token)

    except ExpiredIdTokenError as e:
        return HTTPException(403, detail="Id Token has expired.")

    except RevokedIdTokenError as e:
        return HTTPException(403, detail="Id Token has been revoked")

    except InvalidIdTokenError as e:
        return HTTPException(403, detail="Id Token is invalid")

    except UserDisabledError as e:
        return HTTPException(403, detail="User has been disabled.")

    except CertificateFetchError as e:
        return HTTPException(501, detail="Error fetching certificate")

    except Exception as e:
        #print("Exception:", e)
        return HTTPException(500, detail=e)


# NOTE
# A quick fix to move the JWT from cookie to response so othat the frontend can set the neccessary required headers.
# Reason: Server-Side Google OAuth's redirect requires frontend to use <a> tag instead of the `fetch` api.
#         Additionally, due to the redirects, the `auth/google` endpoint need to return a redirect response to redirect user back to original page
#         Thus, the `auth/google` endpoint returns a `RedirectResponse` with JWT in its cookies.
@router.get('/login/cookies', tags=['authentication'])
async def getJwtFromCookie(request: Request):
    warnings.warn("Function is deprecated in favor of firebase auth")
    jwt_token = request.cookies.get('jwt_token')
    if jwt_token:
        return {'jwt_token': jwt_token}
    else:
        return {}


# Tag it as "authentication" for our docs
@router.get('/login/google', tags=['authentication'])
async def login(request: Request):
    warnings.warn("Function is deprecated in favor of firebase auth")
    if request.session.get("user") is None:
        # Redirect Google OAuth back to our application
        redirect_uri = request.url_for('auth_google')
        #print("redirect_uri:", redirect_uri)
        return await oauth.google.authorize_redirect(request, redirect_uri)
    else:
        return RedirectResponse(CLIENT_BASE_URL)


@router.route('/auth/google', name="auth_google")
async def auth(request: Request):
    warnings.warn("Function is deprecated in favor of firebase auth")
    #print("request.session:", json.dumps(request.session, indent=4))
    registered = False
    # Perform Google OAuth
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')

        # add User to db if new
        isRegistered = False
        userdb = User.objects(email=user.email)
        if userdb:
            userdb = json.loads(userdb.to_json())[0]
            if userdb['email'] == user.email:
                isRegistered = True
        if not isRegistered:
            #print('Creating new User')
            User(email=user.email, name=user.name).save()

    except OAuthError as e:
        #print("oauth_error:", e)
        #print("clientID:", os.environ.get('GOOGLE_CLIENT_ID'))
        #print("clientSecret:", os.environ.get('GOOGLE_CLIENT_SECRET'))
        raise HTTPException(status_code=500, detail=str(e))

    jwt_token = get_token(user)['jwt_token']
    response = RedirectResponse(CLIENT_BASE_URL + "login")
    response.set_cookie("jwt_token", jwt_token,
                        samesite='none', secure=True)
    return response


# Tag it as "authentication" for our docs
@router.get('/logout', tags=['authentication'])
async def logout(request: Request):
    warnings.warn("Function is deprecated in favor of firebase auth")
    # Remove the user
    request.session.pop('user', None)
    request.session.pop('email', None)
    request.session.pop('userid', None)

    response = RedirectResponse(CLIENT_BASE_URL)
    response.delete_cookie("jwt_token")
    return response
