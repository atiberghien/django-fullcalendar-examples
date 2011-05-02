from django.contrib import admin
from schedule.models.calendars import Calendar
from schedule.models.events import  Event
from myagenda.models import MyCalendar, MyEvent

admin.site.unregister(Calendar)
admin.site.register(MyCalendar, admin.ModelAdmin)

admin.site.unregister(Event)
admin.site.register(MyEvent, admin.ModelAdmin)

