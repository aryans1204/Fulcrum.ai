from fastapi import APIRouter, WebSocket
from mongoengine import *

router = APIRouter()

@router.websocket("/api/comms/chat")
async def chat_endpoint(wb: WebSocket):
    await wb.accept()
    while True:
        data = await wb.receive_text()
        '''
            At this section, endpoint will execute the langchain GPT querying to get back the
            response from GPT, and dump to the frontend
        '''
        await wb.send_text("Hello World!!")


