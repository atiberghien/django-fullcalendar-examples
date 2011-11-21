from django.conf.urls.defaults import *
#from schedule.feeds import UpcomingEventsFeed
#from schedule.feeds import CalendarICalendar
from schedule.periods import Month

from .views import create_rule
from myagenda.views import home, coerce_dates_dict, occurrences_to_json, occurrences_to_html
from django.views.generic.list_detail import object_list
from myagenda.models import MyCalendar
from django.views.generic.create_update import create_object
from myagenda.forms import MyEventForm

urlpatterns = patterns('',

    (r'^login/$', 'django.contrib.auth.views.login',
     {'template_name': 'myagenda/login.html'}),
    url(r'^$', home, name="myagenda_home"),

    url(r'^calendar/create/$',
        create_object,
        name="calendar_create",
        kwargs={'model':MyCalendar,
                'post_save_redirect' : '/'}),

    # urls for Calendars
    url(r'^calendar/list/$',
        object_list,
        name="calendar_list",
        kwargs={'queryset':MyCalendar.objects.all(),
                'template_name':'schedule/calendar_list.html'}),

    #Rule
    url(r'^rule/create/$',
        create_rule,
        {'template_name' : 'myagenda/rule_form.html'},
        name="myagenda_create_rule"),

    #Event Urls
    url(r'^event/(?P<event_id>\d+)/$',
        'schedule.views.event',
        name="event"),

    url(r'^event/create/$',
        'schedule.views.create_or_edit_event',
        {'form_class' : MyEventForm,
         'coerce_date_func' : coerce_dates_dict,
         'next' : '/'},
        name='calendar_create_event'),

    url(r'^event/edit/(?P<calendar_slug>[-\w]+)/(?P<event_id>\d+)/$',
        'schedule.views.create_or_edit_event',
        {'form_class' : MyEventForm,
         'template_name' : 'myagenda/edit_event.html',
         'next' : '/'},
        name='edit_event'),

    url(r'^event/(?P<event_id>\d+)/delete/$',
        'schedule.views.delete_event',
        {'next': '/'},
        name="delete_event"),

    #urls for already persisted occurrences
    url(r'^occurrence/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$',
        'schedule.views.occurrence',
        name="occurrence"),

    url(r'^occurrence/cancel/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$',
        'schedule.views.cancel_occurrence',
        name="cancel_occurrence"),

    url(r'^occurrence/edit/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$',
        'schedule.views.edit_occurrence',
        name="edit_occurrence"),

    #urls for unpersisted occurrences
    url(r'^occurrence/(?P<event_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/(?P<second>\d+)/$',
        'schedule.views.occurrence',
        name="occurrence_by_date"),

    url(r'^occurrence/cancel/(?P<event_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/(?P<second>\d+)/$',
        'schedule.views.cancel_occurrence',
        name="cancel_occurrence_by_date"),

    url(r'^occurrence/edit/(?P<event_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/(?P<second>\d+)/$',
        'schedule.views.edit_occurrence',
        name="edit_occurrence_by_date"),

    # AJAX API

    #url for occurrences by encoded data
    url(r'^ajax/(?P<calendar_slug>[-\w]+)/events/json/$',
        'schedule.views.calendar_by_periods_json',
        name="month_calendar_json",
        kwargs={'periods': [Month],
                'nb_periods':1,
                'coerce_date_func':coerce_dates_dict,
                'serialize_occurrences_func':occurrences_to_json}),

    url(r'^ajax/(?P<calendar_slug>[-\w]+)/events/html/$',
        'schedule.views.calendar_by_periods_json',
        name="month_calendar_html",
        kwargs={'periods': [Month],
                'nb_periods':1,
                'coerce_date_func':coerce_dates_dict,
                'serialize_occurrences_func':occurrences_to_html}),

    url(r'^ajax/occurrence/edit_by_code/$',
        'schedule.views.ajax_edit_occurrence_by_code',
        name="ajax_edit_occurrence_by_code"),

    url(r'^ajax/edit_event/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.ajax_edit_event',
        name="ajax_edit_event"),

    url(r'^event_json/$',
        'schedule.views.event_json',
        name="event_json"),

    url(r'^ajax/move_or_resize/$',
        'myagenda.views.ajax_move_or_resize_by_code',
        name="ajax_move_or_resize"),
)
