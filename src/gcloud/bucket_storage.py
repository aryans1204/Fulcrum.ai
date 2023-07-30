import google
from google.cloud import storage
import os


def createBucket(bucket_name: str):
    '''
        Utility for creating a new bucket in GCP Cloud Storage based on a given name
    '''
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = 'STANDARD'
    try:
        new_bucket = storage_client.create_bucket(bucket, location=os.environ["LOCATION"])
        return new_bucket.name
    except google.api_core.exceptions.Conflict:
        #print("bucket exists")
        return bucket_name



def deleteObj(bucket_name: str, blob_name: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(bucket_name)
    blob.reload()
    generation_match_precondition = blob.generation
    blob.delete(if_generation_match=generation_match_precondition)


def deleteBucket(bucket_name: str):
    '''
        Utility for deleting a bucket in GCP Cloud Storage
    '''
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.delete(force=True)


def uploadObj(bucket_name, file_path, fileName):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(fileName)
    generation_match_precondition = 0
    blob.upload_from_filename(file_path, if_generation_match=generation_match_precondition)


