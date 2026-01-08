from kafka import KafkaProducer  
import pandas as pd 
import json
from datetime import datetime
import time 


def create_producer():  
    producer = KafkaProducer(  
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  
    )
    return producer  

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def prepare_record(row):
    record = row.to_dict()
    record["timestamp"] = datetime.utcnow().isoformat()
    return record

def send_to_kafka(producer, data, topic, delay=1):
    i = len(data)
    for index, row in data.iterrows():
        record = prepare_record(row)
        producer.send(topic, value=record)
        if (index + 1) % 10 == 0:
            print(f"Sent {index + 1} of {i} records to Kafka topic {topic}")
        time.sleep(delay)

def main():
    KAFKA_TOPIC = 'amazon-sales-stream'
    CSV_FILE_PATH = '../data/raw/amazon.csv'
    DELAY_BETWEEN_RECORDS = 1

    producer = create_producer()
    data = load_data(CSV_FILE_PATH)
    print(f"Loaded {len(data)} records")
    print(f"Sending data to Kafka topic: {KAFKA_TOPIC}")
    print(f"Delay between records: {DELAY_BETWEEN_RECORDS} second(s)")
    send_to_kafka(producer, data, KAFKA_TOPIC, DELAY_BETWEEN_RECORDS)
    producer.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Process interrupted by user")
    except Exception as e:
        print(f"  Error: {e}")