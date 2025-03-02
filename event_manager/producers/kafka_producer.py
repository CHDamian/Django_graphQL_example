from kafka import KafkaProducer
import json
from event_manager.settings import KAFKA_BROKER_URL

producer = KafkaProducer(
    bootstrap_servers = KAFKA_BROKER_URL,
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

def send_event(event_data):
    producer.send('events', event_data)
    producer.flush()

if __name__ == "__main__":
    send_event("Test Event", "API", "This is a test event")
