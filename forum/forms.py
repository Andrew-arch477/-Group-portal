from django import forms
from django.contrib.auth.models import User
import calendar

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class CalendarForm(forms.Form):
    MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    year = forms.IntegerField(min_value=1900, max_value=2100)