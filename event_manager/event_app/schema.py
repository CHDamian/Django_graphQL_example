from graphene_django import DjangoObjectType
import graphene
from .models import Event
from django.db import models

class EventType(DjangoObjectType):

    class Meta:
        model = Event


class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        source = graphene.String(required=True)
        description = graphene.String()

    event = graphene.Field(EventType)

    def Mutate(self, info, name, source, description = None):
        if source not in Event.EVENT_SOURCES:
            raise ValueError("Unknown source!")
        event = Event.objects.create(name=name, source=source, description=description)
        return CreateEvent(event=event)
    

class UpdateEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)
        description = graphene.String()
    
    event = graphene.Field(EventType)

    def Mutate(self, info, uuid, description = None):
        try:
            event = Event.objects.get(uuid=uuid)
        except Event.DoesNotExist:
            raise Exception("Event not found!")
        
        if description:
            event.description = description
        event.updated_at = models.DateTimeField(auto_now=True)

        event.save()
        return UpdateEvent(event=event)
    

class DeleteEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID(required=True)

    event = graphene.Field(EventType)

    def Mutate(self, info, uuid):
        try:
            event = Event.objects.get(uuid=uuid)
        except Event.DoesNotExist:
            raise Exception("Event not found!")
        
        event.delete()
        return DeleteEvent(success=True)


class Query(graphene.ObjectType):
    events = graphene.List(EventType)

    def resolve_events(self, info):
        return Event.objects.all()
    


