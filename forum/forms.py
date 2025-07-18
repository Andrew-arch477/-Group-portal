from django import forms
from django.contrib.auth.models import User
import calendar
from .models import Grade, Subject, Event, Student
from django.core.exceptions import ValidationError
import requests

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

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'time', 'date', 'month', 'year']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Назва події",
                'autofocus': 'autofocus',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
            }),
            'date': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'month': forms.Select(attrs={
                'class': 'form-control',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }

class GradeForm(forms.ModelForm):
    repository = forms.ChoiceField(choices=[], required=False, label="GitHub Repository")
    
    class Meta:
        model = Grade
        fields = ['student', 'teacher', 'subject', 'grade', 'notes', 'repository']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'grade': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'notes': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(subject_name='Python')

        student = None
        if self.instance and self.instance.pk:
            student = self.instance.student
        elif 'student' in self.initial:
            student = self.initial['student']
        elif 'student' in self.data:
            student_id = self.data.get('student')
            student = Student.objects.get(pk=student_id) if student_id else None
            
        if student and student.github:
            try:
                github_username = student.github.split('/')[-1]
                api_url = f"https://api.github.com/users/{github_username}/repos"
                response = requests.get(api_url)
                if response.status_code == 200:
                    repos = response.json()
                    repo_choices = [(repo['html_url'], repo['name']) for repo in repos]
                    self.fields['repository'].choices = repo_choices
                    if not repos:
                        self.add_error(None, "Учень не має жодного публічного репозиторію на GitHub")
                else:
                    self.add_error(None, "Не вдалося отримати інформацію про репозиторії з GitHub")
            except Exception as e:
                self.add_error(None, f"Помилка при перевірці GitHub: {str(e)}")