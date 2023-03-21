from datetime import datetime, timedelta
from typing import List
from kafka import KafkaProducer
from minio import Minio
import json
import time
import pytz


class MinioToKafka:
    def __init__(self, minio_client: Minio, producer: KafkaProducer) -> None:
        self.minio_client = minio_client
        self.producer = producer
        self.utc = pytz.UTC

    def get_new_object_names(self, bucket_name: str, time_interval: int) -> List[str]:
        current_time = datetime.utcnow()
        past_time = self.utc.localize(current_time - timedelta(seconds=time_interval))

        objects = self.minio_client.list_objects(bucket_name)
        new_objects = [obj for obj in objects if obj.last_modified >= past_time]
        new_object_names = [obj.object_name for obj in new_objects]

        return new_object_names

    def publish_new_objects_to_kafka(self, topic_name: str, new_object_names: List[str]) -> None:
        for name in new_object_names:
            message = {"object_name": name}
            self.producer.send(topic_name, message)


if __name__ == "__main__":
    minio_client = Minio(
        "minio:9000",
        access_key="minio_access_key",
        secret_key="minio_secret_key",
        secure=False,
    )
    producer = KafkaProducer(
        bootstrap_servers=["kafka:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    minio_to_kafka = MinioToKafka(minio_client, producer)

    bucket_name = "my-bucket"
    time_interval = 10
    topic_name = "my-topic"

    while True:
        new_object_names = minio_to_kafka.get_new_object_names(bucket_name, time_interval)
        minio_to_kafka.publish_new_objects_to_kafka(topic_name, new_object_names)
        time.sleep(time_interval)