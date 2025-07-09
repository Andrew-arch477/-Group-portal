from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
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
    path('gradebook/add/', AddGradeView.as_view(), name='add_grade'),
    path('gradebook/edit/<int:pk>/', EditGradeView.as_view(), name='edit_grade'),
    path('gradebook/delete/<int:pk>/', DeleteGradeView.as_view(), name='delete_grade'),
    path('gradebook/student/<int:student_id>/', StudentGradesView.as_view(), name='student_grades'),
    
    path('vote/', VoteView.as_view(), name='vote'),
    path('details_vote/<pk>', DetailsVoteView.as_view(), name='details_vote'),

    path('ads/', AdListView.as_view(), name='ad_list'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('ads/create/', AdCreateView.as_view(), name='ad_create'),
    path('ads/<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('ads/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
]