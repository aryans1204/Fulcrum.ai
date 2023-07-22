<<<<<<< Updated upstream
import uvicorn
import sys
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

=======
>>>>>>> Stashed changes
from starlette.middleware.sessions import SessionMiddleware

<<<<<<< Updated upstream
sys.path.append("/Users/mouse/Documents/GitHub/Fulcrum.ai")
from fastapi import FastAPI
from src.chatbot.endpoints.comms import router as chatbot_comms_router
from src.fulcrum.endpoints.auth import router as auth_router
from src.fulcrum.endpoints.chatbot_ops import router as chatbot_ops_router
from src.fulcrum.endpoints.user import router as user_router
from src.fulcrum.endpoints.docs import router as docs_router

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key='!secret')

routers = [chatbot_comms_router, auth_router, chatbot_ops_router, user_router, docs_router]
for router in routers:
    app.include_router(router)


@app.get('/')
async def home(request: Request):
    user = request.session.get('user')
    if user is not None:
        email = user['email']
        html = (
            f'<pre>Email: {email}</pre><br>'
            '<a href="/docs">documentation</a><br>'
            '<a href="/auth/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/auth/login/google">login</a>')


if __name__ == "__main__":
    uvicorn.run(app)
=======
from fastapi import FastAPI
from fulcrum.endpoints.chatbot_ops import router as chat_router
from fulcrum.endpoints.user import router as user_router
from fulcrum.endpoints.auth import router as auth_router

routers = [chat_router, user_router, auth_router]

mongoengine.connect(host=os.environ["MONGODB_URL"])

app = FastAPI()
for router in routers:
    app.include_router(router)

app.add_middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"])


@app.get("/")
async def main():
    return {"message": "Hello World!!"}



>>>>>>> Stashed changes
