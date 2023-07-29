from fastapi import APIRouter, Form
from typing import Annotated

from starlette.responses import JSONResponse

from fulcrum.db.faq import Question
import time

router = APIRouter()


@router.post('/faq', tags=["faq"])
async def submit_faq(email: Annotated[str, Form()], question: Annotated[str, Form()]):
    timestamp = time.time()
    qn = Question(email=email, question=question)
    qn.save()

    return JSONResponse(qn.to_json())
