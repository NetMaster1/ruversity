from django.urls import path
from . import views

urlpatterns = [
    path('', views.mycourses, name='mycourses'),
    path('new_qestion/<int:subject_id>', views.new_question, name='new_question'),
    path('subject_purchased/<int:subject_id>',views.subject_purchased, name='subject_purchased'),
    path('quiz_api/<int:lecture_id>',views.quiz_api, name='quiz_api'),
    #path('quiz_api_page/<int:lecture_id>',views.quiz_api_page, name='quiz_api_page'),
    path('open_show_quiz_page/<int:lecture_id>',views.open_show_quiz_page, name='open_show_quiz_page'),
    path('reg_answer/<int:quiz_id>/<int:lecture_id>/<int:question_id>',views.reg_answer, name='reg_answer'),
    path('next_quiz_question/<int:quiz_id>/<int:lecture_id>',views.next_quiz_question, name='next_quiz_question'),
]
