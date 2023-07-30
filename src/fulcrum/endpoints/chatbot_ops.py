import datetime
import json
import uuid
from typing import Dict, Any, List, Annotated

from bson import ObjectId
from fastapi.params import Depends
from mongoengine import *
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import EmailStr

from fulcrum.auth.auth_jwt import JWTBearer
from fulcrum.db.chatbot_config import Chatbot
from fulcrum.db.user import User
from fulcrum.models.chatbot import TrainingModel
from gcloud.serverless import deployChatbot, deleteChatbot
from gcloud.vectordb import insertDB, deleteDB
from gcloud.bucket_storage import deleteBucket, createBucket, uploadObj
import shutil
import os
from starlette.requests import Request
router = APIRouter(prefix="/api/chatbot", tags=["api", "chatbot"], dependencies=[Depends(JWTBearer())])


@router.get("/get/all")
async def getAllChatbots():
    """
        Is a development endpoint
    """
    return Chatbot.objects().to_json()


'''@router.get("/getChatbot/{username}/{chatbotID}")
async def giveEndpoint(username: str, chatbotID: str) -> dict:
    """
        Endpoint to get the Cloud Run deployment URL of a given chatbot based on its ID.
    """
    chatbot = Chatbot.objects(chatbot_id=chatbotID)[0]

    return {"url": chatbot.deployedURL}'''


@router.get("/getChatbot/{chatbotID}")
async def getChatbotDetails(chatbotID: str) -> dict:
    """
        Endpoint to get the Chatbot details, including Cloud Run deployment URL of a given chatbot based on its ID.
    """
    try:
      chatbot = Chatbot.objects(chatbot_id=chatbotID)[0].to_json()
      chatbot = json.loads(chatbot)

      return chatbot
    except:
      return {"error": "No such chatbotID exists"}


@router.get("/getChatbots/{userid}", tags=["initChatbot"])
async def init_chatbot(userid: str) -> dict:
    """
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
    """
    user = User.objects(userid=userid)
    if user:
        ids = [c.chatbot_id for c in user[0].chatbotConfigs]
        print("ids:", ids)
        return {"chatbots": ids}
    else:
        print("error, user does not exist")
        return {"error": "No such User exists"}


@router.post("/createChatbot", tags=["createChatbot"], response_model=None)
async def create_chatbot(userid: Annotated[str, Form()], chatbotID: Annotated[str, Form()], personality: Annotated[str, Form()], dataFileName: Annotated[str, Form()]) -> dict[str, str]:
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
    print("chatbotID:", chatbotID)
    url = deployChatbot({"gcs_bucket": chatbotID + userid, "chatbot_id": chatbotID}, userid)
    user = User.objects(userid=userid)[0]
    #print("user:", user.to_json())
    bots = user.chatbotConfigs
    chromadb_index = userid + chatbotID
    chatbot = Chatbot(chatbot_id=chatbotID, chromadb_index=chromadb_index, deployedURL=url,
                      personality=personality, dataFileName=dataFileName, gcs_bucket=chatbotID + userid)
    """chatbotID = str(uuid.uuid4())
    url = deployChatbot({"gcs_bucket":userid+chatbotID, "chatbot_id": chatbotID}, userid)
    user = User.objects.get_queryset(userid=userid)
    bots = user.config
    chatbot = Chatbot(gcs_bucket=userid+chatbot_id, chatbot_id=chatbotID)"""
    bots.append(chatbot)
    chatbot.save()
    user.chatbotConfigs = bots
    user.save()

    return {"endpointURL": url}


@router.delete("/delete/{userid}/{chatbot_id}", tags=["deleteChatbot"])
async def delete_chatbot(userid: str, chatbot_id: str):
    """
        Delete an existing chatbot for user. This endpoit is called by the frontend whenever
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
    """
    user = User.objects(userid=userid)
    if user:
        chatbot = Chatbot.objects(chatbot_id=chatbot_id)[0]
        chatbot.delete()
        deleteChatbot(userid + chatbot_id)

        deleteBucket(userid + chatbot_id)
        deleteDB(userid, chatbot_id)
        return {"msg": "Success"}
    else:
        return {"error": "user not found"}


@router.post("/uploadTrainingData", tags=["trainData"])
async def uploadTraining(file: UploadFile, email: Annotated[EmailStr, Form()]):
    '''
        Endpoint to upload a file, which forms part of the training data of the new created
        chatbot, to the Cloud Storage bucket. This endpoint should be called by the frontend, before
        createChatbot is called, since createChatbot will rely on the created Cloud Storage bucket
        by this endpoint.

        "email" : "email of the user uploading the file",
        chatbotID is the unique identifier; it is no longer a param but will be autogenerated by backend and returned in the response
    '''
    try:
        if not os.path.isdir("images"):
            os.mkdir("images")
    except Exception as e:
        #print(e)
        return {"msg": "Failure1", "error": e}

    file_path = os.getcwd() + "/images" + file.filename.replace(" ", "-")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        f.close()
    userid = str(User.objects(email=email)[0].userid)
    #print('userid:', userid)
    try:
        chatbotID = str(datetime.datetime.now().timestamp()).replace('.', '')
        createBucket(userid + chatbotID)
        #print("created bucket")
        uploadObj(userid + chatbotID, file_path, userid + chatbotID + ".pdf")
        #print("uploaded object")
        insertDB(file_path, userid, chatbotID)
        return {"msg": "Success", "filename": file.filename, "chatbotID": chatbotID}
    except Exception as e:
        #print("error2:", type(e), e)
        return {"msg": "Failure2", "error": e}
