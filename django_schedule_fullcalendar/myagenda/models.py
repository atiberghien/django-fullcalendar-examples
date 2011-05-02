from django.db import models

from schedule.models import Event
from schedule.models.calendars import Calendar

COLOR_TYPE = (
    ('blue', 'blue'),
    ('red', 'red'),
    ('yellow' , 'yellow'),
)
class MyCalendar(Calendar):
    color = models.CharField(max_length=6, choices=COLOR_TYPE)
    nb_slot = models.PositiveIntegerField()

class MyEvent(Event):
    pass
