from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse

from fulcrum.db.user import User
user_router = APIRouter()

from fulcrum.index import oauth
@user_router.get("/api/users", tags=["get_users"])
async def get_users():
    '''
        Endpoint to get all users in the MongoDB collection. Used primarily for internal testing
        purposes.

    '''
    return User.objects()

@user_router.route("/login")
async def login(request: Request):
    '''
        OAuth endpoint for Google login
    '''
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@user_router.post("/api/users/logout", tags=["logout_user"])
async def logout(request: Request):
    '''
        Endpoint for logging out a user based on username and password.
    '''
    request.session.pop('user', None)
    return RedirectResponse(url="/")

@user_router.route("/auth")
async def authenticate(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return {"error":error.error}
    user = token['userinfo']
    if user:
        request.session['user'] = dict(user)
        username = request.session.get('user').get('email')
        userdb = User.objects(username=username)
        if not userdb:
            u = User(username=username)
            u.save()
    return RedirectResponse(url="/")
