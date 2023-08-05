from fastapi import APIRouter, WebSocket, HTTPException
from firebase_admin.auth import verify_id_token, ExpiredIdTokenError, RevokedIdTokenError, InvalidIdTokenError, \
    UserDisabledError, CertificateFetchError

router = APIRouter()


@router.get("/api/auth/verify")
def verify_jwt(self, token: str):
    token_is_valid: bool = False
    try:
        token = verify_id_token(token)
        if token:
            token_is_valid = True
        return token_is_valid

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


