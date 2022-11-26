from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from app_content.models import Lecture, QuizQuestion, QuizAnswer, QuizId


# Create your models here.


class QuizResult (models.Model):

    person = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True, default=1)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(QuizId, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, null=True)
    correct = models.BooleanField(default=False)
   

    def __int__(self):
        return self.id