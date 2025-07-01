from django import forms
from django.contrib.auth.models import User
import calendar
from .models import Grade, Subject

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type here...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Type here...'}))

class MessageForm(forms.Form):
    text = forms.CharField(max_length=850,
        widget=forms.TextInput(attrs={
            'placeholder': 'Напиши щось...'
        })
)
    
class ForumForm(forms.Form):
    title = forms.CharField(max_length=255, label='Title', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type here...'}))

class CalendarForm(forms.Form):
    MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
    month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-control',}))
    year = forms.IntegerField(min_value=1900, max_value=2100, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter year',}))

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'teacher', 'subject', 'grade', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'grade': forms.NumberInput(attrs={'min': 1, 'max': 12}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(subject_name='Python')