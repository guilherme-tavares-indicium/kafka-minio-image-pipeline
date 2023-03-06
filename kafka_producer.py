import os
import time
from minio import Minio
from minio.error import InvalidResponseError
from kafka import KafkaProducer

# Initialize Minio client and bucket name
minio_client = Minio('minio:9000', access_key='minio_access_key', secret_key='minio_secret_key', secure=False)

# Check if bucket exists, create it if not
minio_bucket_name = "my-bucket"
if not minio_client.bucket_exists(minio_bucket_name):
    minio_client.make_bucket(minio_bucket_name)

# Initialize Kafka producer
kafka_topic = 'my-topic'
kafka_bootstrap_servers = ['kafka:9092']
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Initialize list to store already processed files
last_processed_files = []

while True:
    # Get list of objects in Minio bucket
    try:
        objects = minio_client.list_objects(minio_bucket_name)
    except InvalidResponseError as err:
        print(err)
        continue

    # Iterate over objects and publish to Kafka topic if not already processed
    for obj in objects:
        obj_name = obj.object_name
        if obj_name not in last_processed_files:
            # Read data from Minio object
            try:
                data = minio_client.get_object(minio_bucket_name, obj_name)
                file_contents = data.read()
            except InvalidResponseError as err:
                print(err)
                continue

            # Publish data to Kafka topic
            producer.send(kafka_topic, file_contents)
            producer.flush()

            # Add processed file to list
            last_processed_files.append(obj_name)

    # Sleep for 5 seconds before checking for new files again
    time.sleep(5)
