from mongoengine import *
from fastapi import APIRouter, UploadFile, File
from fulcrum.db.chatbot_config import Chatbot
from fulcrum.db.user import User
from gcloud.serverless import deployChatbot, deleteChatbot
from gcloud.vectordb import insertDB, deleteDB
from gcloud.bucket_storage import deleteBucket, createBucket, uploadObj
import shutil
import os
router = APIRouter()

@router.get("/api/chatbot/getChatbot/{username}/{chatbotID}", tags=["getChatbot"])
async def giveEndpoint(username: str, chatbotID: str) -> str:
    '''
        Endpoint to get the Cloud Run deployment URL of a given chatbot based on its ID.
    '''
    chatbot = Chatbot.objects(chatbot_id=chatbotID)

    return {"url": chatbot.deployedURL}

@router.get("/api/chatbot/getChatbots/{username}", tags=["getChatbots"], response_model=None)
async def init_chatbot(username: str) -> Chatbot:
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
    user = User.objects(username=username)
    ids = [c.chatbot_id for c in user.config]
    return {"chatbots": ids}

@router.post("/api/chatbot/createChatbot", tags=["createChatbot"], response_model=None)
async def create_chatbot(username: str, chatbotID: str) -> Chatbot:
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
    url = deployChatbot({"gcs_bucket": chatbotID+username, "chatbot_id":chatbotID}, username)
    user = User.objects(username=username)
    bots = user.config
    chatbot = Chatbot(gcs_bucket=chatbotID+username, chatbot_id=chatbotID)
    bots.append(chatbot)
    chatbot.save()
    user.config = bots
    user.save()

    return {"endpointURL": url}

@router.delete("/api/chatbot/deleteChatbot/{username}/{chatbot_id}", tags=["deleteChatbot"])
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
    deleteChatbot(username+chatbot_id)
    chatbot = Chatbot.objects(chatbot_id=chatbot_id)
    chatbot.delete()
    deleteBucket(username+chatbot_id)
    deleteDB(username, chatbot_id)
    return {"msg": "Success"}

@router.post("/api/chatbot/uploadTrainingData", tags=["trainData"])
async def uploadTraining(file: UploadFile, req):
    '''
        Endpoint to upload a file, which forms part of the training data of the new created
        chatbot, to the Cloud Storage bucket. This endpoint should be called by the frontend, before
        createChatbot is called, since createChatbot will rely on the created Cloud Storage bucket
        by this endpoint.

        req: {
            "username" : "User name of the user deleting the chatbot",
            "chatbotID" : "UUID"
        }
    '''
    try:
        os.mkdir("images")
    except Exception as e:
        return {"msg":"Failure", "error":e}

    file_path = os.getcwd()+"/images"+file.filename.replace(" ", "-")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        f.close()
    try:
        createBucket(req.username+req.chatbotID)
        uploadObj(req.username+req.chatbotID, file_path, req.username+req.chatbotID+".pdf")
        insertDB(file_path, req.username, req.chatbotID)
        return {"msg": "Success"}
    except Exception as e:
        return {"msg": "Failure", "error": e}
    return {"filename" : file.filename}

