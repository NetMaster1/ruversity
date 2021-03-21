from django.urls import path
from . import views

urlpatterns = [
    path('<int:subject_id>', views.review, name='review'),
    path('rating/<int:subject_id>', views.rating, name='rating'),
 
]
