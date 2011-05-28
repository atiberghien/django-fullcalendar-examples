from django import forms
from .models import MyEvent, MyCalendar
from schedule.forms import EventForm, RuleForm
from schedule.models.rules import Rule

class MyEventForm(EventForm):
    end_recurring_period = forms.DateTimeField(widget=forms.SplitDateTimeWidget, required=False)
    calendar = forms.ModelChoiceField(queryset=MyCalendar.objects.all(),
                                      empty_label=None,
                                      required=True)

    def __init__(self, hour24=False, *args, **kwargs):
        super(MyEventForm, self).__init__(*args, **kwargs)

    class Meta(EventForm.Meta):
        model = MyEvent
        fields = ('calendar',
                  'start',
                  'end',
                  'title',
                  'description',
                  'end_recurring_period',
                  'rule')

        exclude = ('creator', 'created_on')
        widgets = {
            'title': forms.TextInput(attrs={'class' : 'text'}),
            'description' : forms.Textarea(attrs={'class' : 'desc', 'cols' : 48, 'rows' : 4}),
        }

class MyRuleForm(RuleForm):
    params = forms.CharField(required=False, label=u'Params', widget=forms.HiddenInput())
    count = forms.CharField(initial='0')
    interval = forms.CharField(initial='1')

    def clean_interval(self):
        interval = self.cleaned_data["interval"]
        self.cleaned_data["params"] += "interval:%s;" % interval
        return self.cleaned_data

    def clean_count(self):
        count = self.cleaned_data["count"]
        self.cleaned_data["params"] += "count:%s;" % count
        return self.cleaned_data

    class Meta:
        model = Rule
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'text'}),
            'description' : forms.Textarea(attrs={'class' : 'desc', 'cols' : 48, 'rows' : 4}),
        }
