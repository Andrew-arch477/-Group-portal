from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from .models import Forum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, CalendarForm
from datetime import datetime
import calendar

# Create your views here.

class Calendar(FormView):
    template_name = 'calendar_event.html'
    form_class = CalendarForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now()

        if 'calendar_html' not in context:
            cal = calendar.HTMLCalendar(firstweekday=0)
            calendar_html = cal.formatmonth(now.year, now.month)
            context['calendar_html'] = calendar_html
            context['month_name'] = calendar.month_name[now.month]
            context['year'] = now.year
            context['css_file'] = 'styles.css'
        return context

    def form_valid(self, form):
        month = int(form.cleaned_data['month'])
        year = int(form.cleaned_data['year'])

        cal = calendar.HTMLCalendar(firstweekday=0)
        calendar_html = cal.formatmonth(year, month)

        return self.render_to_response(self.get_context_data(
            form=form, 
            calendar_html=calendar_html, 
            month_name=calendar.month_name[month], 
            year=year, 
            css_file='styles.css',
        ))

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('forums') 

    def form_valid(self, form): 
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Невірний логін або пароль')
            return self.form_invalid(form)

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

class Forums(View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    
    def get(self, request):
        forums = Forum.objects.all().order_by('-created_date')
        context = self.get_context_data(forums=forums)
        return render(request, 'forums.html', context)
#{% url 'detailed_task' forum_id=forum.id %}

class DetailedForum(View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    
    def get(self, request, forum_id=None):
        forum = Forum.objects.get(id=forum_id)
        forums = Forum.objects.all().order_by('-created_date')
        messages = forum.message_set.all().order_by('created_date')
        context = self.get_context_data(forum=forum, messages=messages, forums=forums)
        return render(request, 'detailed_forum.html', context)

