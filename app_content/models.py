from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class MainSubject(models.Model):
    title = models.CharField(max_length=50)
    date_posted = models.DateTimeField(auto_now_add=True)
    thumbnail_file = models.FileField(upload_to='uploads')
    # author = models.ForeignKey (User, blank=True, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(null=True)

    def __int__(self):
        return self.id


class Lecture(models.Model):
    title = models.CharField(max_length=50)
    date_posted = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='uploads', null=True)
    # author = models.ForeignKey (User, blank=True, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class Transaction(models.Model):
    course = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_bought = models.DateField(auto_now_add=True)
    paid_amoutn = models.FloatField()

    def __int__(self):
        return self.id
