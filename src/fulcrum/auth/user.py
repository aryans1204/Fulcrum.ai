from typing import Optional

from fastapi import HTTPException
from starlette.requests import Request

from fulcrum.db.user import User
from fulcrum.db.utils import get_user_by_id


# Try to get the logged in user
async def validate_user(request: Request) -> Optional[dict]:
    email = request.session.get('email')
    userid = request.session.get('userid')
    print("email:", email)
    print("userid:", userid)
    if userid is not None:
        user = get_user_by_id(userid)
        user_email = user["email"]
        print("user is:", user)
        if user_email != email or not user:
            raise HTTPException(status_code=403, detail='Could not validate credentials.')
        else:
            return user
    else:
        raise HTTPException(status_code=403, detail='Could not validate credentials.')