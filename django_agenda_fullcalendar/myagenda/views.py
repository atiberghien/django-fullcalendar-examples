# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from .forms import MyEventForm, RecurrenceForm
from .models import MyEvent
from agenda.models import Recurrence, Calendar
from datetime import date
from agenda.views.date_based import archive, object_detail
from django.core.urlresolvers import reverse


def current_month_view(request):
    today = date.today()
    calendars = Calendar.objects.all()
    month_events = MyEvent.objects.filter(begin_date__month=today.month).order_by('begin_date')
    return archive(request, 
                   MyEvent.objects.all(),
                   'begin_date',
                   today.year, 
                   month=today.month, 
                   template_name='current_month_view.html', 
                   template_object_name='event', 
                   extra_context={'calendars' : calendars,
                                  'month_events' : month_events})#TODO: add calendar

def show_event(request, slug):
    queryset = MyEvent.objects.all();
    event = queryset.get(slug=slug)
    return object_detail(request, 
                         queryset, 
                         'begin_date', 
                         event.begin_date.year, 
                         event.begin_date.month, 
                         event.begin_date.day, 
                         slug, 
                         template_name='current_month_view.html', 
                         template_object_name='current_event',
                         extra_context={'event_list' : queryset})
    
def create_event(request):
    has_recurrence = False
    if request.method == "POST":
        event_form = MyEventForm(request.POST)
        recurrence_form = RecurrenceForm() # in case of event_form is not valid
        if event_form.is_valid():
            event = event_form.save()
            has_recurrence = request.POST.get('recurrence', None) 
            if has_recurrence:
                has_recurrence = True #instead of "on" in POST
                data = request.POST.copy()
                data['base_event'] = event.id
                recurrence_form = RecurrenceForm(data)
                if recurrence_form.is_valid():
                    recurrence_form.save()
                    return HttpResponseRedirect(reverse('myagenda_current_month_view'))
                else :
                    print "RECURRENCE_FORM", recurrence_form.errors
            else:
                event.save()
                return HttpResponseRedirect(reverse('myagenda_current_month_view'))
        else:
            print "EVENT_FORM", event_form.errors  
    else:
        event_form = MyEventForm()
        recurrence_form = RecurrenceForm()
        
    return render_to_response("event_form.html",
                              {'event_form':event_form,
                               'recurrence_form':recurrence_form,
                               'has_recurrence' : has_recurrence},
                               context_instance=RequestContext(request))
    
def del_event(request, slug):
    event = MyEvent.objects.get(slug=slug)
    if request.method == "POST":
        if event.is_base_event:
            del_base_event = int(request.POST.get('del_base_event', "1"))
            if del_base_event == 1:
                #delete this event and make the first recurrence the new base event
                recurrence = event.recurrence.all()[0]
                first_occur = recurrence.recurrent_events.all().order_by('begin_date','start_time')[0]
                recurrence.recurrent_events.remove(first_occur)
                if recurrence.recurrent_events.count() == 0:
                    recurrence.delete()
                else:
                    recurrence.base_event = first_occur
                    recurrence.save()
                event.delete()
            else:
                #delete this event and all the recurrences
                pass 
        elif event.is_recurrence:
            del_recurrence = int(request.POST.get('del_recurrence', "1"))
            if del_recurrence == 1:
                pass
            elif del_recurrence == 2:
                pass
            else:
                pass
        else:
            event.delete()
        return HttpResponseRedirect(reverse('myagenda_current_month_view'))
    return render_to_response("delevent_form.html",
                              {'event': event},
                               context_instance=RequestContext(request))    
    