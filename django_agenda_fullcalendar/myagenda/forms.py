from django import forms
from agenda.models import Recurrence
from .models import MyEvent

class MyEventForm(forms.ModelForm):
    class Meta:
        model = MyEvent
        fields = ('begin_date', 
                  'start_time', 
                  'end_date',
                  'end_time',
                  'title',
                 'description')
        widgets = {
            'begin_date': forms.DateInput(attrs={'class' : 'begin date datepicker'}),
            'start_time': forms.TimeInput(attrs={'class' : 'begin hour timepicker'}),
            'end_date': forms.DateInput(attrs={'class' : 'end date datepicker'}),
            'end_time': forms.TimeInput(attrs={'class' : 'end hour timepicker'}),
            'title': forms.TextInput(attrs={'class' : 'text'}),
            'description' : forms.Textarea(attrs={'class' : 'desc', 'cols' : 48, 'rows' : 4}),
        }

class RecurrenceForm(forms.ModelForm):
    class Meta:
        model = Recurrence
        fields = ('base_event',
                  'frequency',
                  'start_datetime',
                  'end_datetime',
                  'count',
                  'interval')
        widgets = {
            'start_datetime' : forms.DateTimeInput(attrs={'class' : 'datepicker'}),
            'end_datetime' : forms.DateTimeInput(attrs={'class' : 'datepicker'}),
            'count' : forms.TextInput(attrs={'value' : '0'}),
            'interval' : forms.TextInput(attrs={'value' : '0'}),
            'base_event' : forms.HiddenInput()
        }
