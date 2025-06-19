from django.shortcuts import render
from django.views import View
from .models import Forum
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

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

