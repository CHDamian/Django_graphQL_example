from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import graphene
from .models import Event
from django.db import models
from django_filters import FilterSet, OrderingFilter
import producers.kafka_producer as Producer

class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"
        interfaces = (graphene.relay.Node, )


class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        source = graphene.String(required=True)
        description = graphene.String()

    event = graphene.Field(EventType)

    def mutate(self, info, name, source, description = None):
        if source not in dict(Event.EVENT_SOURCES):
            raise ValueError("Unknown source!")
        event = Event.objects.create(name=name, source=source, description=description)
        return CreateEvent(event=event)
    
class CreateEventAsync(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        source = graphene.String(required=True)
        description = graphene.String()

    success = graphene.Boolean()
    details = graphene.String()

    def mutate(self, info, name, source, description=None):
        if source not in dict(Event.EVENT_SOURCES):
            return CreateEventAsync(success=False, details="Unknown source!")

        event_data = {
            "name": name,
            "source": source,
            "description": description or "",
        }
        Producer.send_event(event_data)

        return CreateEventAsync(success=True, details="")
    

class UpdateEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)
        description = graphene.String()
    
    event = graphene.Field(EventType)

    def mutate(self, info, uuid, description = None):
        try:
            event = Event.objects.get(uuid=uuid)
        except Event.DoesNotExist:
            raise Exception("Event not found!")
        
        if description:
            event.description = description

        event.save()
        return UpdateEvent(event=event)
    

class DeleteEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    event = graphene.Field(EventType)
    success = graphene.Boolean()

    def mutate(self, info, uuid):
        try:
            event = Event.objects.get(uuid=uuid)
        except Event.DoesNotExist:
            return DeleteEvent(success=False)
        
        event.delete()
        return DeleteEvent(success=True)


class EventFilter(FilterSet):
    order_by = OrderingFilter(fields=("created_at", "updated_at", "name"))
    

class Query(graphene.ObjectType):
    all_events = DjangoFilterConnectionField(EventType, filterset_class=EventFilter)
    single_event = graphene.Field(EventType, uuid=graphene.UUID(required=True))

    def resolve_all_events(self, info, **kwargs):
        return Event.objects.all()
    
    def resolve_single_event(self, info, uuid):
        try:
            return Event.objects.get(uuid=uuid)
        except Event.DoesNotExist:
            raise Exception("Event not found!")
    

class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    create_event_async = CreateEventAsync.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()