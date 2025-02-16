from django.db import models
import uuid

# Create your models here.

class Event(models.Model):
    EVENT_SOURCES = [
        ('users', 'Users'),
        ('products', 'Products'),
    ]
    name = models.TextField()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=255, choices=EVENT_SOURCES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    description = models.TextField()
    

