from django.urls import path
from . import views

urlpatterns = [
    path('', views.mycourses, name='mycourses'),
    path('subject_purchased/<int:subject_id>', views.subject_purchased, name='subject_purchased'),
]
