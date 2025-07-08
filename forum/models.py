from django.db import models
from django.contrib.auth.models import User
import calendar
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

class Forum(models.Model):
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, null=True) #reply to


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.middle_name}"
    
    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        unique_together = (("email"),)

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.subject_name

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True,blank=False,null=False, default=None)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    favorite_project = models.TextField(blank=True,null=True)
    github = models.TextField(blank=False,null=False,unique=True, default=None)
    


    def __str__(self):
        return f"{self.first_name} {self.middle_name}"
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        unique_together = (("email"),)

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.grade} ({self.date})"
    
    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"

class Event(models.Model):
    MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]

    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    date = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def get_month_name(self):
        return calendar.month_name[self.month]

class Works(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    title = models.CharField(max_length=40,blank=False,null=False)
    description = models.TextField()
    url = models.URLField(blank=False,null=False)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name

class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def str(self):
        return self.title

class Vote(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False,blank=False)