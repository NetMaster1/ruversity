from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    # zip_code=models.CharField(max_length=100, blank=True)
    # region=models.CharField(max_length=100, blank=True)
    # city=models.CharField(max_length=100, blank=True)
    # street=models.CharField(max_length=100, blank=True)
    # building=models.CharField(max_length=100, blank=True)
    # appartment=models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['user']

    def __int__(self):
        return self.user


class Entity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    entity_type = models.CharField(max_length=50, blank=True)
    tax_id_number = models.CharField(max_length=50, blank=True)
    bin = models.CharField(max_length=50, blank=True)
    bank_account = models.CharField(max_length=50, blank=True)
    # zip_code = models.CharField(max_length=50, blank=True)
    # region = models.CharField(max_length=50, blank=True)
    # city = models.CharField(max_length=50, blank=True)
    # street = models.CharField(max_length=50, blank=True)
    # building = models.CharField(max_length=50, blank=True)
    # office = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    photo = models.FileField(upload_to='uploads')
    background = models.TextField(null=True, max_length=250)

    def __str__(self):
        return self.last_name
