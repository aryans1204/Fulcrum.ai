from mongoengine import *
from fastapi import APIRouter

router = APIRouter()

@router.get("/initChatbot/{username}/{chatbotID}", tags=["initChatbot"])
async def init_chatbot():
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
    return {"response": "Hello World!!"}

@router.post("/createChatbot", tags=["createChatbot"])
async def create_chatbot(req):
    '''
        Create a new chatbot for a user. This endpoint is called by the frontend the first time 
        a user wishes to create a chatbot.
        Endpoint creates a new chatbot based on the params provided, and returns back a URL of the
        deployed chatbot. Handles all internal first time infra setup, like Cloud Storage bucket, 
        MongoDB insertion handling, Vertex AI Matching Engine index deployment, and VPC Peering

        req: {
            "username" : "User name of the user creating the chatbot",
            
        }

        res: {
            "endpointURL" : "Returns back the Cloud Run URL which serves as the backend to chatbot",
            "error" : {None if everything works out, otherwise one of}:

            101: GCloud error
            102: Bad MongoDB query error
            103: User chatbot limit exceeded, user has created more chatbots than are allowed.
        }
    '''

    @router.post("/deleteChatbot", tags=["deleteChatbot"])
    async def delete_chatbot(req):
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
