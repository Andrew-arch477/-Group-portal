from django.db import models

# Create your models here.
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
    phone = models.CharField(max_length=15)
    email = models.EmailField()



    def __str__(self):
        return f"{self.first_name} {self.middle_name}"
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        unique_together = (("email"),)
