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

@login_required(login_url='/login/')
def home(request):
    calendars = MyCalendar.objects.all()
    if calendars.count() == 0:
        return HttpResponseRedirect(reverse("calendar_list"))

    return calendar_by_periods(request,
                               calendars[0].slug,
                               periods=[Month],
                               template_name='myagenda/current_month_view.html',
                               extra_context={'calendars' : calendars})


def create_event(request):
    return create_or_edit_event(request,
                                template_name='myagenda/event_form.html',
                                form_class=MyEventForm,
                                coerce_date_func=coerce_dates_dict,
                                next='/')

def edit_event(request, event_id):
    return create_or_edit_event(request,
                                event_id=event_id,
                                template_name='myagenda/event_form.html',
                                form_class=MyEventForm,
                                next='/')

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


def occurrences_to_json(occurrences, user):
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

def occurrences_to_html(occurences, user):
    res = ""
    for occ in occurences:
        rnd = loader.get_template('myagenda/event.html')
        resp = rnd.render(Context({'occ':occ}))
        res += resp
    return res


