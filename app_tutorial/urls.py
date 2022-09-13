from django.urls import path
from . import views

urlpatterns = [

    path ('tutorial', views.tutorial, name='tutorial'),
    path ('video/<int:video_id>', views.video, name='video'),

]