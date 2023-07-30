import os
import chromadb
from chromadb import HttpClient
from gcloud.pdfparser2 import parsePDF
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain.embeddings import OpenAIEmbeddings

def insertDB(file_path: str, username: str, chatbot_id: str):
    '''
        Utility to insert a PDF into the ChromaDB database as Sentence transformer vectors
    '''
    print("inserting db...")
    chunks = parsePDF(file_path)
    client = HttpClient(host=os.environ["CHROMA_URL"], port=os.environ["CHROMA_PORT"])
    print("chroma_url:", f'{os.environ["CHROMA_URL"]}:{os.environ["CHROMA_PORT"]}')
    openai_ef = OpenAIEmbeddingFunction(
                api_key=os.environ["OPENAI_API_KEY"],
                model_name="text-embedding-ada-002"
            )

    collection = client.get_or_create_collection(name=username+chatbot_id)
    ids = []
    texts = []
    metadatas = []
    cur_len = collection.count()
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    for c in chunks:
        cur_len += 1
        ids.append("id"+str(cur_len))
        texts.append(c)
        metadatas.append({str(cur_len): c})
    
    embeds = embeddings.embed_documents(texts)
    collection.add(
        documents=texts,
        metadatas=metadatas,
        embeddings=embeds,
        ids=ids
    )

def deleteDB(username: str, chatbot_id: str):
    '''
        Utility for deleting a collection in the ChromaDB database. This is a 
        non-reversible action.
    '''
    client = HttpClient(host=os.environ["CHROMA_URL"], port=os.environ["CHROMA_PORT"])

    collection = client.delete_collection(name=username+chatbot_id)


