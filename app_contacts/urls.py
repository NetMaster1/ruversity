from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacts, name='contacts'),
    path('help/', views.help, name='help'),
    path('termsofuse/', views.termsofuse, name='termsofuse'),
    path('partneship/', views.partnership, name='partnership'),
    path('socialmedia/', views.socialmedia, name='socialmedia'),
    path('career/', views.career, name='career'),
    path('email/', views.email, name='email'),
    path('personal_data/', views.personal_data, name='personal_data'),

]
