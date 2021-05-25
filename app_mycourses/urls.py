from django.urls import path
from . import views

urlpatterns = [
    path('', views.mycourses, name='mycourses'),
    path('new_qestion/<int:subject_id>', views.new_question, name='new_question'),
    path('subject_purchased/<int:subject_id>',views.subject_purchased, name='subject_purchased'),
]
