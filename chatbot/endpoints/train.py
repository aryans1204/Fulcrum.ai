from fastapi import APIRouter
from mongoengine import *
from ../../fulcrum/models/chatbot import Chatbot
import os
router = APIRouter()

@router.get("/api/train/load_data")
async def load_data(chatbot: Chatbot):
    '''
        The endpoint is called by initChatbot on Fulcrum, after the Cloud Run instance is created.
        The endpoint takes a chatbot as a query parameter, and loads in environment variables
        from the provided chatbot model.
    '''
    os.environ["VERTEX_AI_URI"] = chatbot["vertex_url"]
    os.environ["VERTEX_INDEX"] = chatbot["chatbot_id"]
    os.environ["VERTEX_CLOUD_STORAGE"] = chatbot["vertex_bucket"]
    os.environ["GCS_BUCKET"] = chatbot["gcs_bucket"]


    
