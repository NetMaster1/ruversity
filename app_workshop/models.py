from django.db import models


# Create your models here.
class Country(models.Model):
    country = models.CharField(max_length=50)

    def __int__(self):
        return self.id
