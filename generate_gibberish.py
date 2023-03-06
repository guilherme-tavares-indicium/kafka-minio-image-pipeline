from io import BytesIO
import random
import string

from minio import Minio
from minio.error import InvalidResponseError

# Set up Minio client
minio_client = Minio(
    "minio",
    access_key="minio_access_key",
    secret_key="minio_secret_key",
    secure=False
)

# Generate random content for file
def generate_content():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Create and upload file to Minio bucket
def create_file():
    filename = ''.join(random.choices(string.ascii_lowercase, k=10)) + '.txt'
    content = generate_content()
    try:
        minio_client.fput_object(
            "my-bucket",
            filename,
            content
        )
        print(f"Created file {filename} with content:\n{content}")
    except InvalidResponseError as err:
        print(err)

if __name__ == '__main__':
    create_file()
