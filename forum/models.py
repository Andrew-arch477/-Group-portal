from django.db import models

# Create your models here.

class Forum(models.Model):
    title = models.CharField(max_length=200)