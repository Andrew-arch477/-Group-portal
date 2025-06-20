from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forums/', Forums.as_view(), name='forums'),
    path('detailed_forum/<int:forum_id>/', DetailedForum.as_view(), name='detailed_forum'),
    path('eventcalendar/', Calendar.as_view(), name='calendar_event'),
]