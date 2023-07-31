import os
import time
import warnings
from datetime import datetime
from datetime import timedelta

import jwt
from fastapi import Depends, Request
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token, ExpiredIdTokenError, RevokedIdTokenError, InvalidIdTokenError, \
    UserDisabledError, CertificateFetchError

from fulcrum.db.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/google")


# Helper to read numbers using var envs
def cast_to_number(_id):
    temp = os.environ.get(_id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None


# Configuration
API_SECRET_KEY = os.environ.get('SECRET_KEY') or None
if API_SECRET_KEY is None:
    raise BaseException('Missing SECRET_KEY env var.')
API_ALGORITHM = os.environ.get('API_ALGORITHM') or 'HS256'
API_ACCESS_TOKEN_EXPIRE_MINUTES = cast_to_number('API_ACCESS_TOKEN_EXPIRE_MINUTES') or 15


# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


# Create token internal function
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=100)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt


# Create token for an email
def create_token(data: dict):
    access_token_expires = timedelta(minutes=100)
    access_token = create_access_token(data=data, expires_delta=access_token_expires)
    return access_token


def decodeJWT(token: str) -> dict:
    try:
        return jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION


class JWTBearerOld(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        warnings.warn("Function is deprecated in favor of firebase auth")
        super(JWTBearerOld, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerOld, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials)[0]:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            if not self.verify_jwt(credentials.credentials)[1]:
                raise HTTPException(status_code=403, detail="User not registered.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> (bool, bool):
        token_is_valid: bool = False
        try:
            payload = decodeJWT(jwt_token)
        except:
            payload = None
        registered = None
        if payload:
            token_is_valid = True
            registered = payload["registered"]

        return token_is_valid, registered


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials)[0]:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            if not self.verify_jwt(credentials.credentials)[1]:
                raise HTTPException(status_code=403, detail="User not registered.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> (bool, bool):
        token_is_valid: bool = False
        is_registered = False
        try:
            id_token = verify_id_token(token)
            if id_token:
                token_is_valid = True
                userdb = User.objects(email=id_token["email"])
                if userdb:
                    is_registered = True
            return token_is_valid, is_registered

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


def jsonify_jwt(token):
    return {"access_token": token, "token_type": "bearer"}
