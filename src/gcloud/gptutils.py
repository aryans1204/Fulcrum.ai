import langchain
from langchain.llms import OpenAIChat
from langchain.chains import RetrievalQA
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import chromadb
from chromadb import HttpClient

from fulcrum.models.chatbot import Chatbot
import os
import ctypes

def initLLM():
    llm = OpenAIChat(
        temperature=int(os.environ["temperature"]),
        model_name=os.environ["gpt_model"],
        top_p=float(os.environ["top_p"]),
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )
    global __chatbot__
    __chatbot__ = llm

    client = HttpClient(host=os.environ["chroma_url"], port=os.environ["chroma_port"])
    openai_ef = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

    vectordb = Chroma(collection_name=os.environ["chroma_index"], client=client, embedding_function=openai_ef)

    retriever = VectorStoreRetriever(vectorstore=vectordb)
    global __chain__
    __chain__ = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

def queryGPT(msg: str) -> str:
    PROMPT = """
        Prompt: Do not create assumption or give suggestions or give opinions from your own. \
        If you don't know the answer, just say you don't know. \
        Don't ask the user if you need to find out the answer. \
    """

    if "__chain__" in globals():
        qa = ctypes.cast(id(globals()["__chain__"]), ctypes.py_object).value
        ans = qa({"query":"Question: " + msg + PROMPT})
        return ans["result"]

    else:
        initLLM()
        qa = ctypes.cast(id(globals()["__chain__"]), ctypes.py_object).value
        ans = qa({"query":"Question: " + msg + PROMPT})
        return ans["result"]

