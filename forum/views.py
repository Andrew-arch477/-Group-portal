from django.shortcuts import render
from django.views import View
from .models import Forum
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Forums(LoginRequiredMixin, View):
    def get_context_data(self, **kwargs):
        context = kwargs
        return context
    
    def get(self, request):
        forums = Forum.objects.all()
        context = self.get_context_data(forums=forums)
        return render(request, 'forums.html', context)
