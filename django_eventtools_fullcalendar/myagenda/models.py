from django.db import models 
from eventtools.models import EventModel, OccurrenceModel, GeneratorModel, ExclusionModel

class Event(EventModel):
    pass
    
class Generator(GeneratorModel): 
    event = models.ForeignKey(Event, related_name="generators")
    
class Occurrence(OccurrenceModel): 
    event = models.ForeignKey(Event, related_name="occurrences") 
    generated_by = models.ForeignKey(Generator, blank=True, null=True, related_name="occurrences")

class Exclusion(ExclusionModel): 
    event = models.ForeignKey(Event, related_name="exclusions")
