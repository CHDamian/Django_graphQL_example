from django.db import models
from django.utils.timezone import now
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
    updated_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = now()
        super().save(*args, **kwargs)
    

