from fastapi import APIRouter, WebSocket, Depends

from src.fulcrum.auth.user import get_user
from src.gcloud.gptutils import queryGPT

router = APIRouter(prefix="/api/comms", dependencies=[Depends(get_user)])


@router.websocket("/chat")
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


