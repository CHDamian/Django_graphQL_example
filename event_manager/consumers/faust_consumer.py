import faust
import sys
import os
import django
from asgiref.sync import sync_to_async

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_manager.settings")
django.setup()

from event_app.models import Event

app = faust.App("event_consumer", broker="kafka://kafka:9092", value_serializer="json")

class EventModel(faust.Record, serializer="json"):
    name: str
    source: str
    description: str = ""

events_topic = app.topic("events", value_type=EventModel)

@app.agent(events_topic)
async def process_event(events):
    """Konsumer do przetwarzania eventów."""
    print("Received event!!!")
    async for event in events:
        await save_event(event)

@sync_to_async
def save_event(event: EventModel):
    """Zapisuje event do bazy SQLite w Django."""
    Event.objects.create(
        name=event.name,
        source=event.source,
        description=event.description or "",
    )
