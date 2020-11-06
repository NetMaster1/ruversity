from django.urls import path
from . import views

urlpatterns = [
    path('', views.studio, name='studio'),
    path('create_new_subject', views.create_new_subject, name='create_new_subject'),
    path('create_new_lecture/<int:subject_id>',
         views.create_new_lecture, name='create_new_lecture'),
    path('edit_subject/<int:subject_id>',
         views.edit_subject, name='edit_subject'),
    path('edit_lecture/<int:lecture_id>',
         views.edit_lecture, name='edit_lecture'),
    path('delete_lecture/<int:lecture_id>',
         views.delete_lecture, name='delete_lecture'),
    path('video/<int:lecture_id>', views.video, name='video')
]
