import boto3
from botocore.client import Config

# Connect to our local MinIO Docker container
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

BUCKET_NAME = "agentbucket"

def upload_file_to_s3(file_content: bytes, filename: str):
    """Uploads a file to the MinIO S3 bucket."""
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=file_content
        )
        return f"Successfully uploaded {filename} to S3."
    except Exception as e:
        raise Exception(f"Failed to upload to S3: {str(e)}")



def list_files_in_s3():
    """Lists all files in the S3 bucket."""
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    "filename": obj['Key'],
                    "size_bytes": obj['Size'],
                    "last_modified": obj['LastModified'].isoformat()
                })
        return files
    except Exception as e:
        raise Exception(f"Failed to list S3 files: {str(e)}")