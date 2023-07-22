import os
import chromadb
from chromadb.config import Settings

def insertDB(file_path: str, username: str, chatbot_id: str):
    '''
        Utility to insert a PDF into the ChromaDB database as Sentence transformer vectors
    '''
    chunks = parsePDF(file_path)
    client = chromadb.Client(
        Settings(
            chroma_api_impl="rest",
            chroma_server_host=os.environ["CHORMA_URL"],
            chroma_server_http_port=os.environ["CHROMA_PORT"]
        )
    )

    collection = client.get_or_create_collection(name=username+chatbot_id)
    ids = []
    texts = []
    metadatas = []
    cur_len = collection.count()

    for c in chunks:
        cur_len += 1
        ids.append("id"+str(cur_len))
        texts.append(c)
        metadatas.append({"id": c})

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
    client = chromadb.Client(
        Settings(
            chroma_api_impl="rest",
            chroma_server_host=os.environ["CHROMA_URL"],
            chroma_server_http_port=os.environ["CHROMA_PORT"]
        )
    )

    collection = client.delete_collection(name=username+chatbot_id)


