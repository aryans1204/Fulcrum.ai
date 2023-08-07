from fastapi import APIRouter, WebSocket, HTTPException

from chatbot.endpoints.auth import verify_jwt
from src.gcloud.gptutils import queryGPT

router = APIRouter()


@router.websocket("/api/comms/chat/auth")
async def chat_endpoint(wb: WebSocket, id_token: str):
    is_auth = verify_jwt(id_token)
    await wb.accept()
    if is_auth is True:
        while True:
            data = await wb.receive_text()
            '''
                At this section, endpoint will execute the langchain GPT querying to get back the
                response from GPT, and dump to the frontend
            '''
            res = queryGPT(data)
            await wb.send_text(res)
    else:
        return HTTPException(401, detail="Invalid authentication credentials.")


