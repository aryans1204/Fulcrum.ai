from src.gcloud.gptutils import queryGPT
from src.gcloud.vectordb import insertDB, deleteDB
import uuid
import re
import os

file_path = "/home/aryan/Downloads/FinTech Hackcelerator Project Coordinator (Events).pdf"
username = 'aryans1204'
cid = str(uuid.uuid4())

def test_query_gpt():
    os.environ["temperature"] = os.environ["TEMPERATURE"]
    os.environ["top_p"] = os.environ["TOP_P"]
    os.environ["gpt_model"] = os.environ["GPT_MODEL"]
    os.environ["chroma_index"] = username+cid
    os.environ["chroma_url"] = os.environ["CHROMA_URL"]
    os.environ["chroma_port"] = os.environ["CHROMA_PORT"]
    insertDB(file_path, username, cid)
    ans = queryGPT("What are the key responsibilities")
    print("ans: ", ans)
    deleteDB(username, cid)
    assert ans is not None
    assert len(re.findall("GFH", ans)) > 0


