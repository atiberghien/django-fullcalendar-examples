from django.conf.urls.defaults import * 
from eventtools.views import EventViews 
from .models import Event

views = EventViews(event_qs=Event.eventobjects.all())

urlpatterns = patterns('', 
    url(r'^', include(views.urls)),
)
