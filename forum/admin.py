from django.contrib import admin
from forum.models import Teacher, Student, Subject, Grade, Event, Forum, Works

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Event)
admin.site.register(Forum)
admin.site.register(Works)