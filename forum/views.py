from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, DetailView, UpdateView
from django.views.generic.edit import FormView
from .models import Student, Forum, Message, Grade, Event, Works, Subject
from .forms import LoginForm, MessageForm, CalendarForm, GradeForm, ForumForm, EventForm
from datetime import datetime
import calendar
from django.contrib.auth.models import User

class Calendar(FormView):
    template_name = 'calendar_event.html'
    form_class = CalendarForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now()

        context['events'] = kwargs.get('events', Event.objects.all())

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

        events = Event.objects.filter(month=month, year=year)

        events_by_day = {}
        for event in events:
            if event.date:
                day = event.date
                if day not in events_by_day:
                    events_by_day[day] = []
                events_by_day[day].append(event)

        cal = calendar.HTMLCalendar(firstweekday=0)
        calendar_html = cal.formatmonth(year, month)

        for day, list_events_day in events_by_day.items():
            events_html = ''.join(
                f"<div class='event'>{event.name}</div>"
                for event in list_events_day
            )
            search = f">{day}<"
            replace = f">{day}<br>{events_html}<"
            calendar_html = calendar_html.replace(search, replace)

        return self.render_to_response(self.get_context_data(
            form=form,
            calendar_html=calendar_html,
            month_name=calendar.month_name[month],
            year=year,
            css_file='styles.css',
            events=events
        ))

class Event_delete(DeleteView):
    model = Event
    template_name = 'calendar_event_delete.html'
    success_url = reverse_lazy('calendar_event')

class Event_update(FormView):
    template_name = 'calendar_event_update.html'
    form_class = EventForm
    success_url = reverse_lazy('calendar_event')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        event_id = self.kwargs.get('pk')
        event = Event.objects.get(pk=event_id)
        kwargs['instance'] = event
        return kwargs

    def form_valid(self, form):
        form.save() 
        return super().form_valid(form)
    
    def get_object(self):
        event_id = self.kwargs.get('pk')
        return get_object_or_404(Event, pk=event_id)

class Event_create(FormView):
    template_name = 'calendar_event_create.html'
    form_class = EventForm
    success_url = reverse_lazy('calendar_event')

    def form_valid(self, form):
        Event.objects.create(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            time=form.cleaned_data['time'],
            date=form.cleaned_data['date'],
            month=form.cleaned_data['month'],
            year=form.cleaned_data['year']
        )
        return super().form_valid(form)

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

class Forums(FormView):
    form_class = ForumForm
    template_name = 'forums.html'
    success_url = '/forums/'
    
    def dispatch(self, request, *args, **kwargs):
        self.action = None
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        forums = Forum.objects.all().order_by('-created_date')
        user_role = self.request.user.profile.role
        context = self.get_context_data(forums=forums, role=user_role)
        context["css_file"] = 'styles.css'
        return render(request, 'forums.html', context)
    
    def post(self, request, *args, **kwargs):
        if "delete_id" in request.POST:
            forum_id = request.POST.get("delete_id")
            forum = Forum.objects.get(id=forum_id)

            forum.delete()
            
            return redirect('forums')
        elif "edit_id" in request.POST:
            edit_id = self.request.POST.get("edit_id")
            forum = Forum.objects.get(id=edit_id)
            forum.title = request.POST.get('title')
            forum.save()
            return redirect("forums")
            

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return redirect('login')
        title = form.cleaned_data['title']

        edit_id = self.request.POST.get("edit_id")

        if self.action == "edit" and edit_id:
            forum = Forum.objects.get(id=edit_id)
            forum.title = title
            forum.save()
        else:
            Forum.objects.create(
            title=title
        )

        return redirect('forums')

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
        if not self.request.user.is_authenticated:
            return redirect('login')
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for student in context["students"]:
            if not student.username.startswith('@'):
                student.username = '@'+student.username
        return context

class DetailsPortfolioView(DetailView):
    template_name = "details/details_portfolio.html"
    model = Student

    def get_context_data(self, **kwargs):
        context = super(DetailsPortfolioView, self).get_context_data(**kwargs)
        context['students'] = Student.objects.get(pk=self.kwargs['pk'])
        context['works'] = Works.objects.filter(user_id=User.objects.get(pk=self.kwargs['pk']))
        return context

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        if not obj.username.startswith('@'):
            obj.username = '@'+obj.username
        return obj

class GradebookHomeView(TemplateView):
    template_name = 'gradebook.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = Grade.objects.all().order_by('-date')
        context['students'] = Student.objects.all()
        context['subject'] = Subject.objects.get(subject_name='Python')
        return context


class AddGradeView(FormView):
    template_name = 'add_grade.html'
    form_class = GradeForm
    success_url = '/gradebook'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = Subject.objects.get(subject_name='Python')
        return context

class DeleteGradeView(DeleteView):
    model = Grade
    template_name = 'delete_grade.html'
    success_url = '/gradebook'

class EditGradeView(UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'edit_grade.html'
    success_url = '/gradebook'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = Subject.objects.get(subject_name='Python')
        return context

class StudentGradesView(TemplateView):
    template_name = 'student_grades.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        context['student'] = Student.objects.get(pk=student_id)
        context['grades'] = Grade.objects.filter(student=student_id).order_by('-date')
        context['subject'] = Subject.objects.get(subject_name='Python')
        return context


