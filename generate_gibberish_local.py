import os
import io
import random
import string
from minio import Minio
from minio.error import InvalidResponseError

# Set up Minio client
minio_client = Minio(
    "localhost:9000",
    access_key="minio_access_key",
    secret_key="minio_secret_key",
    secure=False
)

# Create the data folder if it doesn't exist
if not os.path.exists('data'):
    os.mkdir('data')

# Check if bucket exists, create it if not
minio_bucket_name = "my-bucket"
if not minio_client.bucket_exists(minio_bucket_name):
    minio_client.make_bucket(minio_bucket_name)

# while True:
for some_file in range(30):
    # Generate a random filename
    filename = ''.join(random.choices(string.ascii_lowercase, k=10))

    # Generate some random content for the file
    content = ''.join(random.choices(string.ascii_lowercase + ' ', k=100))
    content_as_bytes = content.encode('utf-8')
    content_as_a_stream = io.BytesIO(content_as_bytes)

    try:
        minio_client.put_object(
            "my-bucket",
            filename,
            content_as_a_stream,
            length=len(content_as_bytes)
        )
        print(f"Created file {filename} with content:\n{content}")
    except InvalidResponseError as err:
        print(err)

    # Sleep for 5 seconds before creating the next file
    # time.sleep(5)