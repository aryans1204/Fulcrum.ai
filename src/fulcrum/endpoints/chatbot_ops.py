from typing import Dict, Any, List

from fastapi.params import Depends
from mongoengine import *
from fastapi import APIRouter, UploadFile, File

from fulcrum.auth.auth_jwt import JWTBearer
from fulcrum.db.chatbot_config import Chatbot
from fulcrum.db.user import User
from gcloud.serverless import deployChatbot, deleteChatbot
from gcloud.vectordb import insertDB, deleteDB
from gcloud.bucket_storage import deleteBucket, createBucket, uploadObj
import shutil
import os
from starlette.requests import Request
router = APIRouter(prefix="/api/chatbot", tags=["api", "chatbot"], dependencies=[Depends(JWTBearer())])


@router.get("/getChatbot/{username}/{chatbotID}", tags=["getChatbot"])
async def giveEndpoint(username: str, chatbotID: str) -> dict[str, Any]:
    '''
        Endpoint to get the Cloud Run deployment URL of a given chatbot based on its ID.
    '''
    chatbot = Chatbot.objects(chatbot_id=chatbotID)


@router.get("/getChatbots/{username}", tags=["getChatbots"], response_model=None)
async def init_chatbot(username: str) -> dict[str, list[Any]]:
    '''
        initialize chatbot endpoint is called from the Fulcrum frontend each time
        a user accesses a previously created chatbot. The endpoint is responsible for
        calling the Cloud Run macros, and initializing the serverless chatbot on a container
        on Cloud Run.

        req: {
            "username" : "User name of the user to run the MongoDB query",
            "chatbotID" : "frontend can use any RNG or UUID generator to create this, as long
            as its consistent in the MongoDB data schemas"
        }

        res: {
            "endpointURL" : "URL for the Cloud Run chatbot, to call chatbot endpoints from the server",
            "error": {None if everything works out, otherwise one of}:

            101: GCloud error
            102: Bad MongoDB query error
            103: User token limit exceeded, cannot access chatbot due to OpenAI usage limits
        }
    '''


@router.get("/test", name="chatbot_test")
async def chatbot_test(request: Request):
    return {"message": "test"}


@router.post("/createChatbot", tags=["createChatbot"], response_model=None)
async def create_chatbot(username: str, chatbotID: str) -> dict[str, str]:
    '''
        Create a new chatbot for a user. This endpoint is called by the frontend the first time 
        a user wishes to create a chatbot. Frontend should first call the upload_file endpoint.
        Endpoint creates a new chatbot based on the params provided, and returns back a URL of the
        deployed chatbot. Handles all internal first time infra setup, like Cloud Storage bucket,
        MongoDB insertion handling, Vertex AI Matching Engine index deployment, and VPC Peering

        req: {
            "username" : "User name of the user creating the chatbot"
        }

        res: {
            "endpointURL" : "Returns back the Cloud Run URL which serves as the backend to chatbot",
            "error" : {None if everything works out, otherwise one of}:

            101: GCloud error
            102: Bad MongoDB query error
            103: User chatbot limit exceeded, user has created more chatbots than are allowed.
        }
    '''
    return {"response": "Hello World!!"}


@router.delete("/deleteChatbot/{username}/{chatbot_id}", tags=["deleteChatbot"])
async def delete_chatbot(username: str, chatbot_id: str):
    '''
        Delete an existing chatbot for s uer. This endpoit is called by the frontend whenever
        user wants to delete an existing chatbot. The endpoint performs cleanup of Google Cloud 
        infra resources, as well as updating the MongoDB schema for the user. Returns error
        or success.

       req: {
           "username" : "User name of the user deleting the chatbot",
           "chatbotID" : "existing chatbotID"
       }

       res: {
           "error" : {None if everything works out, otherwise one of}:

           101: GCloud error
           102: Bad MongoDB error
       }
   '''
    return {"response": "Hello World!!"}


@router.post("/uploadTrainingData", tags=["trainData"])
async def uploadTraining(file: UploadFile):
    '''
        Endpoint to upload a file, which forms part of the training data of the new created
        chatbot, to the Cloud Storage bucket. This endpoint should be called by the frontend, before
        createChatbot is called, since createChatbot will rely on the created Cloud Storage bucket
        by this endpoint.

        req: {
            "username" : "Username of the user uploading the file",
            "chatbotID" : "UUID"
        }
    '''
    return {"filename": file.filename}
