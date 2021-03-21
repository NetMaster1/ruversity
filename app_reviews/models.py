from django.db import models
from django.contrib.auth.models import User
from app_content.models import MainSubject

# Create your models here.


class Review (models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE)

    def __int__(self):
        return self.id
