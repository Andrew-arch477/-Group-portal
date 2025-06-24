from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, TemplateView, ListView, DetailView
from .models import Forum, Message, Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, MessageForm, CalendarForm
from datetime import datetime
import calendar


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

class DetailedForum(FormView):
    form_class = MessageForm
    template_name = 'detailed_forum.html'

    def dispatch(self, request, *args, **kwargs):
        self.forum_id = kwargs.get('forum_id')
        self.forum = None
        self.action = None
        if self.forum_id:
            self.forum = Forum.objects.get(id=self.forum_id)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        forums = Forum.objects.all().order_by('-created_date')
        messages = self.forum.message_set.all().select_related('reply').order_by('created_date')
        context = self.get_context_data(forum=self.forum, messages=messages, forums=forums)
        context["css_file"] = 'styles.css'
        return render(request, 'detailed_forum.html', context)

    def post(self, request, *args, **kwargs):
        if "delete_id" in request.POST:
            message_id = request.POST.get("delete_id")
            message = Message.objects.get(id=message_id)

            message.delete()
            
            return redirect('detailed_forum', forum_id=self.forum_id)
        elif "edit_id" in request.POST:
            self.action = "edit"
            

        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        text = form.cleaned_data['text']
        reply_to_id = self.request.POST.get("reply_to_id")
        edit_id = self.request.POST.get("edit_id")

        if self.action == "edit" and edit_id:
            message = Message.objects.get(id=edit_id, user=self.request.user)
            message.text = text
            message.save()

        elif reply_to_id:
            reply = Message.objects.get(id=reply_to_id)
            Message.objects.create(
                forum=self.forum,
                user=self.request.user,
                text=text,
                reply=reply
            )
        else:
            Message.objects.create(
                forum=self.forum,
                user=self.request.user,
                text=text
            )

        return redirect('detailed_forum', forum_id=self.forum_id)

class PortfolioView(ListView):
    template_name = "portfolio.html"
    model = Student
    context_object_name = 'students'


class DetailsPortfolioView(DetailView):
    template_name = "details/details_portfolio.html"
    model = Student
    context_object_name = 'student'