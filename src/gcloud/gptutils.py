import langchain
from langchain.llms import OpenAIChat
from langchain.chains import RetrievalQA
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import chromadb
from chromadb.config import Settings
from src.fulcrum.models.chatbot import Chatbot
import os
import ctypes

def initLLM():
    llm = OpenAIChat(
        temperature=os.environ["temperature"],
        model_name=os.environ["gpt_model"],
        top_p=os.environ["top_p"],
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )
    __chatbot__ = llm

    client = chromadb.Client(
        Settings(
            chroma_api_impl="rest",
            chroma_server_host=os.environ["chroma_url"],
            chroma_server_http_port=os.environ["chroma_port"]
        )
    )

    retriever = Chroma(collection_name=os.environ["chroma_index"], client=client)
    __chain__ = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

def queryGPT(msg: str) -> str:
    PROMPT = """
        Prompt: Do not create assumption or give suggestions or give opinions from your own. \
        If you don't know the anser, just say you don't know. \
        Don't ask the user if you need to find out the answer. \
    """

    if __chain__ in globals():
        qa = ctypes.cast(id(globals()["__chain__"]), ctypes.py_object).value
        ans = qa({"query":"Question: " + msg + PROMPT})
        return ans["result"]

    else:
        initLLM()
        qa = ctypes.cast(id(globals()["__chain__"]), ctypes.py_object).value
        ans = qa({"query":"Question: " + msg + PROMPT})
        return ans["result"]

