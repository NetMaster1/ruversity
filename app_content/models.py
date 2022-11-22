from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from . storage import OverwriteStorage
import uuid
from app_accounts.models import Author
from durationwidget.widgets import TimeDurationWidget

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Price(models.Model):
    regular = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2)

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
    # author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True, default=1)
    price = models.ForeignKey(Price, on_delete=models.DO_NOTHING)
    author_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
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
    discount_programs = models.BooleanField(default=True, null=True)
    length = models.IntegerField(default=0)#length in seconds
    length_1 = models.DurationField(null=True, default='00:00:00')#length in hours:min:seconds

    def __int__(self):
        return self.id

class Library(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True, default=1)
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE, null=True)
    video_file = models.FileField(upload_to='uploads', null=True)
    length = models.IntegerField(default=0)#length in seconds
    length_1 = models.DurationField(null=True)#length in hours:min:seconds
    size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __it__(self):
        return self.id

class Section(models.Model):
    course = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    length = models.IntegerField(default=0)
    length_1 = models.DurationField(null=True)
    title = models.CharField(max_length=100)
    enumerator = models.IntegerField(null=True)

    def __int__(self):
        return self.id

class Lecture(models.Model):
    title = models.CharField(max_length=100, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    video_file = models.FileField(upload_to='uploads', null=True)
    video_uuid = models.UUIDField(default=uuid.uuid4)#CDN
    dash_url = models.CharField(max_length=512, null=True)#CDN
    hls_url = models.CharField(max_length=512, null=True)#CDN
    widevine_url = models.CharField(max_length=512, null=True)#CDN
    playready_url = models.CharField(max_length=512, null=True)#CDN
    fairplay_url = models.CharField(max_length=512, null=True)#CDN
    fairplay_certificate_url = models.CharField(max_length=512, null=True)#CDN
    processing_state = models.DecimalField(max_digits=1,decimal_places=0,default=0)#CDN
    subtitle_file = models.FileField(upload_to='uploads', null=True, blank =True)
    translation_file = models.FileField(upload_to='uploads', null=True, blank=True)
    # author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True, default=1)
    blocked = models.BooleanField(default=False)
    free = models.BooleanField(default=False)
    length = models.IntegerField(default=0)#overall length in secs
    length_1 = models.DurationField(null=True)#duration in hours:min:sec
    size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    enumerator = models.IntegerField(null=True)

    # def get_absolute_file_upload_url(self):
    #     return MEDIA_URL + self.file_upload.url

    def __int__(self):
        return self.id

class AdditionalMaterialLink(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    url_link = models.URLField(null=True)

    # def get_absolute_file_upload_url(self):
    #     return MEDIA_URL + self.file_upload.url

    def __int__(self):
        return self.id

class AdditionalMaterialFile(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    additional_file = models.FileField(upload_to='uploads/', null=True)

    # def get_absolute_file_upload_url(self):
    #     return MEDIA_URL + self.file_upload.url

    def __int__(self):
        return self.id

class Quiz (models.Model):
    quiz_title = models.CharField(max_length=100, null=True)
    subject = models.ForeignKey(MainSubject, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)

    def __int__(self):
        return self.id

class QuizQuestion (models.Model):
    question = models.CharField(max_length=100, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)

    def __int__(self):
        return self.id

class QuizAnswer (models.Model):
    answer = models.CharField(max_length=100, null=True)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, null=True)
    correct = models.BooleanField(default=False)

    def __int__(self):
        return self.id

class Transaction(models.Model):
    date_created = models.DateField(auto_now_add=True)
    money_paid = models.BooleanField(default=False)#check if money have been paid
    payment_id = models.CharField(max_length=100, null=True)
    # course = models.ForeignKey(MainSubject, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(MainSubject, on_delete=models.CASCADE)
    # author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT, null=True, default=1)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_paid = models.DateField(null=True)
    paid_amount = models.FloatField(null=True)
    money_transfer = models.BooleanField(default=False)#check after money transfer to the author
    date_transfer = models.DateField(null=True)
    transferred_amount = models.FloatField(null=True)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
