from django.contrib import admin
from forum.models import Teacher, Student, Subject, Event

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Event)
