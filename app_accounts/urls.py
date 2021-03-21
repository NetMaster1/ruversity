from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register_user'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('change_email', views.change_email, name='change_email'),
    path('change_password', views.change_password, name='change_password'),
    path('change_name', views.change_name, name='change_name'),
]
