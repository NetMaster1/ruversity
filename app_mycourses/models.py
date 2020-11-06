from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class Subject_purchased(models.Model):
    title = models.CharField(max_length=50)
    purchase_date = models.DateField(auto_now_add=True)
    thumbnail_file = models.FileField(upload_to='uploads')
    # author = models.ForeignKey (User, blank=True, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(null=True)

    def __int__(self):
        return self.id
