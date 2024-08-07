from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date


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

class DiscountOn(models.Model):
    discount_on = models.BooleanField(default=True)

    def __int__(self):
        return self.id


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TempImage(models.Model):
    temp_thumbnail_file = models.FileField(upload_to='uploads')

    def __it__(self):
        return self.id

class MainSubject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    prerequisite = models.TextField(null=True)
    # date_posted = models.DateField(default=date.today)
    # date_posted = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateField(auto_now_add=True)
    thumbnail_file = models.FileField(upload_to='uploads')
    # thumbnail_file = models.ImageField(upload_to='uploads', width_field='width_field', height_field='height_field')
    # width_field=models.IntegerField(default=750)
    # height_field=models.IntegerField(default=422)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    price = models.ForeignKey(Price, on_delete=models.DO_NOTHING)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    percent = models.CharField(max_length=50, default='0%')
    total = models.IntegerField(default=0)  # Общее число баллов
    quantity = models.IntegerField(default=0)  # Кол-во оценок
    av_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)  # average rating
    transactions = models.IntegerField(default=0)#counter
    reviews = models.IntegerField(default=0)#counter
    ready = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    discount_programs = models.BooleanField(default=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __int__(self):
        return self.id


class Section(models.Model):
    course = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    length = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    title = models.CharField(max_length=100)

    def __int__(self):
        return self.id

class Lecture(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='uploads', null=True)
    subtitle_file = models.FileField(upload_to='uploads', null=True)
    translation_file = models.FileField(upload_to='uploads', null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    blocked = models.BooleanField(default=False)
    free = models.BooleanField(default=False)
    length = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    size_mb = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # def get_absolute_file_upload_url(self):
    #     return MEDIA_URL + self.file_upload.url

    def __int__(self):
        return self.id


class Transaction(models.Model):
    course = models.ForeignKey(MainSubject, on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_bought = models.DateField(auto_now_add=True)
    paid_amount = models.FloatField(null=True)

    def __int__(self):
        return self.id

# class Bestseller (models.Model):
#     subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
#     transactions = models.IntegerField()

#     def __int__(self):
#         return self.id


class Rating (models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __int__(self):
        return self.id


class Badword (models.Model):
    badword = models.CharField(max_length=50)

    def __int__(self):
        return self.id


class Keyword (models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    keyword = models.CharField(max_length=50)

    def __int__(self):
        return self.id


class Paypal (models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=50)

    def __int__(self):
        return self.id


class Credit_card_type(models.Model):
    type = models.CharField(max_length=50)

    def __int__(self):
        return self.id


class Credit_card (models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    card_number = models.CharField(max_length=50)
    card_type = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __int__(self):
        return self.id


class Bank_account (models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    country = models.CharField(max_length=50)
    entity_name = models.CharField(max_length=50, blank=True)
    itin = models.CharField(max_length=50, blank=True)
    bin = models.CharField(max_length=50, blank=True)
    bank_account = models.CharField(max_length=50, blank=True)
    account = models.CharField(max_length=50)
    ready = models.BooleanField(default=False)

    def __int__(self):
        return self.id


class Main_method (models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    method = models.CharField(max_length=50)

    def __int__(self):
        return self.id


class Cart(models.Model):
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __int__(self):
        return self.id


class Question(models.Model):
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    date_posted = models.DateField(auto_now_add=True)

    def __int__(self):
        return self.id


class Answer(models.Model):
    subject=models.ForeignKey(MainSubject, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=100)
    date_posted = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.content

# class AverageRating(models.Model):
#     subject = models.ForeignKey(MainSubject, on_delete=models.DO_NOTHING)
#     total = models.IntegerField() #Общее число баллов
#     quantity = models.IntegerField()  #Кол-во оценок
#     av_rating=models.DecimalField(max_digits=3, decimal_places=1, default=0)

#     def __int__(self):
#         return self.id

#     def average(self):
#             average_1 = round(float(self.total / self.quantity), 2)
#             average_2 = average_1/5*100
#             average_3 = str(average_2)
#             percent = '%'
#             average = average_3 + percent
#             print(average)
#             return average
