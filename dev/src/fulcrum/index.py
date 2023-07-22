import uvicorn
import sys
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from starlette.middleware.sessions import SessionMiddleware

sys.path.append("/Users/estherteo/fulcrum.ai/fulcrum.ai-backend/Fulcrum.ai")
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
