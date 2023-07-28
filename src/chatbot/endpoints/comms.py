from fastapi import APIRouter, WebSocket
from src.gcloud.gptutils import queryGPT

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
        res = queryGPT(data)
        await wb.send_text(res)


