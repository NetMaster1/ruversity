from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Price(models.Model):
    regular = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def __float__(self):
        return self.regular

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MainSubject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    date_posted = models.DateTimeField(auto_now_add=True)
    thumbnail_file = models.FileField(upload_to='uploads')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.DO_NOTHING)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)

    def __int__(self):
        return self.id


class Lecture(models.Model):
    title = models.CharField(max_length=50)
    date_posted = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='uploads', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class Transaction(models.Model):
    course = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_bought = models.DateField(auto_now_add=True)
    paid_amount = models.FloatField(null=True)

    def __int__(self):
        return self.id

class Bestseller (models.Model):
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    transactions = models.IntegerField()

    def __int__(self):
        return self.id


class Rating (models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __int__(self):
        return self.id

class AverageRating(models.Model):
    subject = models.ForeignKey(MainSubject, on_delete=models.DO_NOTHING)
    total = models.IntegerField()
    quantity=models.IntegerField()

    def __int__(self):
        return self.id

    def average(self):
            return float(self.total) / self.quantity
