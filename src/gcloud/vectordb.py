import os
import chromadb
from chromadb import HttpClient
from gcloud.pdfparser2 import parsePDF
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

def insertDB(file_path: str, username: str, chatbot_id: str):
    '''
        Utility to insert a PDF into the ChromaDB database as Sentence transformer vectors
    '''
    chunks = parsePDF(file_path)
    client = HttpClient(host=os.environ["CHROMA_URL"], port=os.environ["CHROMA_PORT"])
    openai_ef = OpenAIEmbeddingFunction(
                api_key=os.environ["OPENAI_API_KEY"],
                model_name="text-embedding-ada-002"
            )

    collection = client.get_or_create_collection(name=username+chatbot_id, embedding_function=openai_ef)
    ids = []
    texts = []
    metadatas = []
    cur_len = collection.count()

    for c in chunks:
        cur_len += 1
        ids.append("id"+str(cur_len))
        texts.append(c)
        metadatas.append({str(cur_len): c})

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

def deleteDB(username: str, chatbot_id: str):
    '''
        Utility for deleting a collection in the ChromaDB database. This is a 
        non-reversible action.
    '''
    client = HttpClient(host=os.environ["CHROMA_URL"], port=os.environ["CHROMA_PORT"])

    collection = client.delete_collection(name=username+chatbot_id)


