from src.gcloud.vectordb import insertDB, deleteDB
import uuid
import chromadb
from chromadb import HttpClient
from chromadb.utils import embedding_functions
import os

username = 'aryans1204'
file_path = '/home/aryan/Downloads/FinTech Hackcelerator Project Coordinator (Events).pdf'
uid = str(uuid.uuid4())

def test_insert_database():
    insertDB(file_path, username, uid)
    client = HttpClient(host=os.environ["CHROMA_URL"], port=os.environ["CHROMA_PORT"])

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ["OPENAI_API_KEY"],
                model_name="text-embedding-ada-002"
            )
    collection = client.get_collection(username+uid, embedding_function=openai_ef)
    assert collection.count() > 0

def test_delete_database():
    deleteDB(username, uid)
    client = HttpClient(host=os.environ["CHROMA_URL"], port=os.environ["CHROMA_PORT"])
    try:
        collection = client.get_collection(username+uid)
        assert False
    except:
        assert True
