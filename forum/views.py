from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from .models import Forum, Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, MessageForm

# Create your views here.

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('forums') #

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
        if self.forum_id:
            self.forum = Forum.objects.get(id=self.forum_id)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        forums = Forum.objects.all().order_by('-created_date')
        messages = self.forum.message_set.all().order_by('created_date')
        context = self.get_context_data(forum=self.forum, messages=messages, forums=forums)
        context["css_file"] = 'styles.css'
        return render(request, 'detailed_forum.html', context)
    
    def form_valid(self, form):
        text=form.cleaned_data['text']
        Message.objects.create(
            forum=self.forum,
            user=self.request.user,
            text=text
        )
        return redirect('detailed_forum', forum_id=self.forum_id)

