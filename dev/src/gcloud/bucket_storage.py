from google.cloud import storage
import os

def createBucket(bucket_name: str):
    '''
        Utility for creating a new bucket in GCP Cloud Storage based on a given name
    '''
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = 'STANDARD'
    new_bucket = storage_client.create_bucket(bucket, location=os.environ["LOCATION"])
    return new_bucket.name

def deleteBucket(bucket_name: str):
    '''
        Utility for deleting a bucket in GCP Cloud Storage
    '''
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

def uploadObj(bucket_name, file_path, fileName):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(fileName)

    blob.upload_from_filename(file_path, if_generation_match=generation_match_precondition)



