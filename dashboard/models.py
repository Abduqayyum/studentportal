
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    desciption = models.TextField()

    class Meta:
        verbose_name_plural = "Notes"

    def __str__(self):
        return self.title


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    desciption = models.TextField() 
    subject = models.CharField(max_length=50)
    due = models.DateTimeField(default=datetime.now)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.subject


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)


    def __str__(self):
        return self.title

