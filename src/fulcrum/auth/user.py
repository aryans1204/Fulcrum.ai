from typing import Optional

from fastapi import HTTPException
from starlette.requests import Request

from fulcrum.db.user import User
from fulcrum.db.utils import get_user_by_id
from fulcrum.auth.auth_jwt import CREDENTIALS_EXCEPTION


# Try to get the logged in user
async def get_user(request: Request) -> Optional[dict]:
    email = request.session.get('email')
    userid = request.session.get('userid')
    print("email:", email)
    print("userid:", userid)
    if userid is not None:
        user = get_user_by_id(userid)
        if not user:
            return None
        else:
            return user
    else:
        raise CREDENTIALS_EXCEPTION