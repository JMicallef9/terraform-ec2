import boto3
import os

def upload_to_s3():
    "Uploads a local file to an S3 bucket."
    bucket = os.environ["BUCKET_NAME"]
    input_key = os.environ["INPUT_KEY"]
    local_file = os.environ["LOCAL_FILE"]

    s3 = boto3.client("s3")

    s3.upload_file(local_file, bucket, input_key)

if __name__ == "__main__":
    upload_to_s3()