from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forums/', Forums.as_view(), name='forums'),
    path('detailed_forum/<int:forum_id>/', DetailedForum.as_view(), name='detailed_forum'),

    path('eventcalendar/', Calendar.as_view(), name='calendar_event'),
    path('eventcreate/', Event_create.as_view(), name='calendar_event_create'),
    path('eventdelete/<int:pk>/', Event_delete.as_view(), name='calendar_event_delete'),
    path('eventupdate/<int:pk>/', Event_update.as_view(), name='calendar_event_update'),

    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('details_portfolio/<pk>', DetailsPortfolioView.as_view(), name='details_portfolio'),
    
    path('gradebook/', GradebookHomeView.as_view(), name='gradebook'),
    path('add/', AddGradeView.as_view(), name='add_grade'),
    path('edit/<int:pk>/', EditGradeView.as_view(), name='edit_grade'),
    path('delete/<int:pk>/', DeleteGradeView.as_view(), name='delete_grade'),
    path('student/<int:student_id>/', StudentGradesView.as_view(), name='student_grades'),
]