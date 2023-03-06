#!/bin/bash

# Wait until the Kafka broker is ready
echo "Waiting for Kafka broker to become available..."

# checks whether the TCP port is available for use
while ! nc -z kafka 9092; do
  sleep 0.1
done

echo "Kafka broker is available!"

# Create the Kafka topic if it doesn't exist
echo "Creating Kafka topic..."
/usr/local/kafka/bin/kafka-topics.sh \
    --create \
    --if-not-exists \
    --zookeeper zookeeper:2181 \
    --replication-factor 1 \
    --partitions 1 \
    --topic test-topic

echo "Starting Kafka producer..."

# Run the Kafka producer in the background
python kafka_producer.py &

# Keep the container running
tail -f /dev/null
