from django.urls import path
from .views import *


urlpatterns = [
    path('forums/', Forums.as_view(), name='forums'),
    path('detailed_forum/<int:forum_id>/', DetailedForum.as_view(), name='detailed_forum'),
]