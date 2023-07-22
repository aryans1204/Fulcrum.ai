from src.gcloud.bucket_storage import uploadObj, createBucket, deleteBucket
import os
import uuid
from google.cloud import storage

username = 'aryans1204'
cid = str(uuid.uuid4())
bucket_name = username+cid
file_path = "/home/aryan/Downloads/FinTech Hackcelerator Project Coordinator (Events).pdf"
file_name = "test"

def test_create_bucket():
    name = createBucket(bucket_name)
    client = storage.Client()
    bucket = client.bucket(name)
    assert bucket.exists()

def test_upload_file():
    uploadObj(bucket_name, file_path, file_name)
    client = storage.Client()
    blobs = client.list_blobs(bucket_name)
    for blob in blobs:
        assert blob.name == file_name

def test_delete_bucket():
    deleteBucket(bucket_name)
    client = storage.Client()
    try:
        bucket = client.bucket(bucket_name)
        assert False

    except:
        assert True



