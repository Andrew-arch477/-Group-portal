from django.urls import path
from .views import *


urlpatterns = [
    path('forums/', Forums.as_view(), name='forums'),
]