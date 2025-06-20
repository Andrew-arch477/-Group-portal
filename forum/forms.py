from django import forms
from django.contrib.auth.models import User
import calendar

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type here...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Type here...'}))

class MessageForm(forms.Form):
    text = forms.CharField(max_length=850,
        widget=forms.TextInput(attrs={
            'placeholder': 'Напиши щось...'
        })
)

class CalendarForm(forms.Form):
    MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
    month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-control',}))
    year = forms.IntegerField(min_value=1900, max_value=2100, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter year',}))