import uvicorn
import os
import boto3
from pathlib import Path
from urllib.parse import urlparse


def download_s3_folder(s3_uri, local_dir=None):
    """
    Download the contents of a folder directory
    Args:
        s3_uri: the s3 uri to the top level of the files you wish to download
        local_dir: a relative or absolute directory path in the local file system
    """
    AWS_S3_CREDS = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_KEY"),
    }
    s3 = boto3.resource("s3", **AWS_S3_CREDS)
    bucket = s3.Bucket(urlparse(s3_uri).hostname)
    s3_path = urlparse(s3_uri).path.lstrip("/")
    if local_dir is not None:
        local_dir = Path(local_dir)
    for obj in bucket.objects.filter(Prefix=s3_path):
        target = (
            obj.key
            if local_dir is None
            else local_dir / Path(obj.key).relative_to(s3_path)
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        if obj.key[-1] == "/":
            continue
        bucket.download_file(obj.key, str(target))


if __name__ == "__main__":
    # download latest model from s3
    download_s3_folder(
        "s3://agc-rl-bucket/assim.model/", "server/tfmodels/assim.model/"
    )
    download_s3_folder("s3://agc-rl-bucket/heat.model/", "server/tfmodels/heat.model/")
    download_s3_folder(
        "s3://agc-rl-bucket/water.model/", "server/tfmodels/water.model/"
    )
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
