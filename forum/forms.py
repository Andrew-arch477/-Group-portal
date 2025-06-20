from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class MessageForm(forms.Form):
    text = forms.CharField(max_length=850,
        widget=forms.TextInput(attrs={
            'placeholder': 'Напиши щось...'
        })
)
