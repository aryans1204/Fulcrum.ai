from src.gcloud.serverless import deployChatbot, deleteChatbot
import uuid
import re
import os

from src.gcloud.bucket_storage import createBucket, deleteBucket
username = 'aryans1204'
uid = str(uuid.uuid4())

def test_deploy_chatbot():
    createBucket(username+uid)
    chatbot = {"chatbot_id":uid, "gcs_bucket":username+uid}
    url = deployChatbot(chatbot, username)
    print(url)
    deleteBucket(username+uid)
    assert len(re.findall("https.*app", url)) > 0

def test_file_removal():
    assert not os.path.exists(f"{os.environ['YAML_DIR']}/services_temp.yaml")


