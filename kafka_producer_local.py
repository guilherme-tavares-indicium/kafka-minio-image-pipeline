import os
import time
from kafka import KafkaProducer
from typing import Set, List

# The Kafka broker hostname and port number
KAFKA_BROKER: str = "kafka:9092"

# The Kafka topic to publish messages to
KAFKA_TOPIC: str = "test-topic"

# The directory to watch for new files
DATA_DIR: str = "data"

# The set of files processed in the last loop
last_processed_files: Set[str] = set()


def main() -> None:
    # Create a Kafka producer instance
    producer: KafkaProducer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])

    # Keep looping indefinitely
    while True:
        # Get a list of all files in the data directory
        files: List[str] = os.listdir(DATA_DIR)

        # Get the set of new files added since the last loop
        new_files: Set[str] = set(files) - last_processed_files

        # Loop through each new file in the directory
        for file_name in new_files:
            # Skip directories and files that don't end in .txt
            if os.path.isdir(file_name) or not file_name.endswith(".txt"):
                continue

            # Open the file and read its contents
            with open(os.path.join(DATA_DIR, file_name), "r") as file:
                lines: List[str] = file.readlines()

            # Publish each line of the file as a separate message to the Kafka topic
            for line in lines:
                producer.send(KAFKA_TOPIC, line.encode())

            # Print a message indicating that the file has been processed
            print(f"Processed file {file_name}")

        # Adds the last_processed_files variable to the current set of files
        last_processed_files.update(files)

        # Wait for 5 seconds before checking for new files
        time.sleep(5)


if __name__ == "__main__":
    main()

