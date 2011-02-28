from django.db import models
from agenda.models import Event, create_recurrence, Recurrence
from django.db.models import signals

class MyEvent(Event):
    pass


def create_myrecurrence(sender, instance, created, **kwargs):
    create_recurrence(sender, instance, created, event_class=MyEvent)

signals.post_save.connect(create_myrecurrence, Recurrence, dispatch_uid="example-ajax.myagenda.models")