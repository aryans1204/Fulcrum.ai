from fastapi import APIRouter, Form
from typing import Annotated

from starlette.responses import JSONResponse

from fulcrum.db.faq import Question
import time

router = APIRouter()


@router.post('/faq', tags=["faq"])
async def submit_faq(name: Annotated[str, Form()], email: Annotated[str, Form()], message: Annotated[str, Form()]):
    timestamp = time.time()
    qn = Question(email=email, name=name, content=message)
    qn.save()

    return JSONResponse(qn.to_json())
