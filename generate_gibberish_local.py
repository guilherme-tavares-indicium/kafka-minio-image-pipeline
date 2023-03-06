import os
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
    filename = ''.join(random.choices(string.ascii_lowercase, k=10)) + '.txt'
    filepath = os.path.join('data', filename)

    # Generate some random content for the file
    content = ''.join(random.choices(string.ascii_lowercase + ' ', k=100))

    # Write the content to the file
    with open(filepath, 'w') as f:
        f.write(content)

    print(f'Created file {filename}')

    # put the file in the minio bucket
    try:
        minio_client.fput_object(
            "my-bucket",
            filename,
            filepath
        )
        print(f"Created file {filename} with content:\n{content}")
    except InvalidResponseError as err:
        print(err)

    # Sleep for 5 seconds before creating the next file
    # time.sleep(5)
    