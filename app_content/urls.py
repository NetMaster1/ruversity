from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subject/<int:subject_id>', views.subject, name='subject'),
]
