from typing import Optional, Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
from starlette.responses import JSONResponse
import time

from src.fulcrum.auth.user import get_user

router = APIRouter(prefix="/docs", dependencies=[Depends(get_user)]) # This dependency protects our endpoint!

"""@router.route('/openapi.json')
async def get_open_api_endpoint(request: Request, user: Optional[dict] = Depends(get_user)):  # This dependency protects our endpoint!
    response = JSONResponse(get_openapi(title='FastAPI', version=1, routes=router.routes))
    return response
"""


@router.get('/', tags=['documentation'])  # Tag it as "documentation" for our docs
async def get_documentation(request: Request):
    response = get_swagger_ui_html(openapi_url='/openapi.json', title='Documentation')
    return response


@router.post('/faq', tags=["faq"])
async def submit_faq(email: Annotated[str, Form()], category: Annotated[str, Form()], question: Annotated[str, Form()]):
    timestamp = time.time()
    response = dict(email=email, category=category, question=question, timestamp=timestamp)

    # TODO: link to db

    return response

