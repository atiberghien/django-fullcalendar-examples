from django.contrib import admin 
from eventtools.admin import EventAdmin, OccurrenceAdmin
from .models import Event, Occurrence

admin.site.register(Event,EventAdmin(Event),show_exclusions=True)
admin.site.register(Occurrence, OccurrenceAdmin(Occurrence))

