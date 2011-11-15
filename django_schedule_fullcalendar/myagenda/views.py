# Create your views here.

from .forms import MyEventForm, MyRuleForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from schedule.views import create_or_edit_event, calendar_by_periods
from django.utils import simplejson
from schedule.periods import Month
from myagenda.models import MyCalendar
from datetime import datetime, timedelta
from schedule.utils import encode_occurrence
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

@login_required(login_url='/login/')
def home(request):
    calendars = MyCalendar.objects.all()
    if calendars.count() == 0:
        return HttpResponseRedirect(reverse("calendar_list"))

    current_calendar = calendars[0]

    return calendar_by_periods(request,
                               calendars[0].slug,
                               periods=[Month],
                               template_name='myagenda/current_month_view.html',
                               extra_context={'calendars' : calendars,
                                              'current_calendar' : current_calendar,
                                              'now' : datetime.now()})

def create_rule(request, template_name):
    if request.method == "POST":
        rule_form = MyRuleForm(request.POST)
        if rule_form.is_valid():
            rule_form.save()
        else:
            print rule_form.errors
    else:
        rule_form = MyRuleForm()

    return render_to_response(template_name,
                              {'rule_form':rule_form},
                              context_instance=RequestContext(request))


def coerce_dates_dict(date_dict):
    try:
        start = float(date_dict.get("start"))
        start = datetime.fromtimestamp(start // 1000)
    except:
        start = datetime.now()
    try:
        end = float(date_dict.get("end"))
        end = datetime.fromtimestamp(end // 1000)
    except:
        end = None
    return (start, end)


def occurrences_to_json(request, occurrences, user):
    occ_list = []
    for occ in occurrences:
        original_id = occ.id
        occ_list.append({
            'id':encode_occurrence(occ),
            'title' : occ.title,
            'start' : occ.start.isoformat(),
            'end': occ.end.isoformat(),
            'recurring':bool(occ.event.rule),
            'persisted':bool(original_id),
            'description':occ.description.replace('\n', '\\n'),
            'allDay':False,
            'cancelled' : occ.cancelled
        })
    return simplejson.dumps(occ_list)

def occurrences_to_html(request, occurences, user):
    return render_to_string('myagenda/event.html',
                            {'occurences':occurences},
                            context_instance=RequestContext(request))
