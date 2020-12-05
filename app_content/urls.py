from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subject/<int:subject_id>', views.subject, name='subject'),
    path('gen_search/', views.gen_search, name='gen_search'),
    path('main_page/', views.main_page, name='main_page'),
]
