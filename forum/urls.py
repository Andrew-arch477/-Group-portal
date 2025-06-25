from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forums/', Forums.as_view(), name='forums'),
    path('detailed_forum/<int:forum_id>/', DetailedForum.as_view(), name='detailed_forum'),
    path('eventcalendar/', Calendar.as_view(), name='calendar_event'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('details_portfolio/<pk>', DetailsPortfolioView.as_view(), name='details_portfolio'),
    path('gradebookhome/', GradebookHomeView.as_view(), name='gradebook'),
    path('add/', AddGradeView.as_view(), name='add_grade'),
    path('student/<int:student_id>/', StudentGradesView.as_view(), name='student_grades'),
]