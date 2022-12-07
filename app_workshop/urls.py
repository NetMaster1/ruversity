from django.urls import path
from . import views

urlpatterns = [
    path('studio', views.studio, name='studio'),
    path('create_new_subject', views.create_new_subject, name='create_new_subject'),
    path('delete_subject/<int:subject_id>', views.delete_subject, name='delete_subject'),

    path('edit_subject/<int:subject_id>',views.edit_subject, name='edit_subject'),
    path('create_new_section/<int:subject_id>', views.create_new_section, name='create_new_section'),
    path('edit_section_title/<int:section_id>', views.edit_section_title, name='edit_section_title'),
    path('delete_section/<int:subject_id>/<int:section_id>',views.delete_section, name='delete_section'),

    path('create_new_lecture/<int:subject_id>/<int:section_id>',views.create_new_lecture, name='create_new_lecture'),
    path('edit_lecture/<int:lecture_id>',views.edit_lecture, name='edit_lecture'),
    path('edit_lecture_title/<int:lecture_id>',views.edit_lecture_title, name='edit_lecture_title'),
    path('delete_lecture/<int:lecture_id>',views.delete_lecture, name='delete_lecture'),
    path('delete_lecture_videofile/<lecture_id>', views.delete_lecture_videofile, name="delete_lecture_videofile"),
    path('lecture_update_videofile/<int:subject_id>/<int:section_id>/<lecture_id>', views.lecture_update_videofile, name="lecture_update_videofile"),


    path('video/<int:subject_id>/<int:lecture_id>', views.video, name='video'),
    path('agreement/<int:subject_id>', views.agreement, name='agreement'),
    path('agree/<int:subject_id>', views.agree, name='agree'),
    path('disagree/<int:subject_id>', views.disagree, name='disagree'),
    path('author_profile', views.author_profile, name='author_profile'),
    path('create_author_page', views.create_author_page, name='create_author_page'),
    path('author_page/<int:user_id>', views.author_page, name='author_page'),
    path('edit_author_page/<int:user_id>', views.edit_author_page, name='edit_author_page'),
    path('credit_card', views.credit_card, name='credit_card'),
    path('paypal', views.paypal, name='paypal'),
    path('main_method', views.main_method, name='main_method'),
    path('edit_main_method', views.edit_main_method, name='edit_main_method'),
    path('bank_account', views.bank_account, name='bank_account'),
    path('transactions', views.transactions, name='transactions'),
    path('GeneratePDF', views.GeneratePDF.as_view(), name="GeneratePDF"),
    #path('question_answer', views.question_answer, name="question_answer"),
    path('answer/<int:subject_id>/<int:question_id>', views.answer, name="answer"),
    path('upload_multiple_files/<int:subject_id>', views.upload_multiple_files, name="upload_multiple_files"),
   
    path('bulk_lecture_enumerator_update/<int:subject_id>', views.bulk_lecture_enumerator_update, name="bulk_lecture_enumerator_update"),
    path('lecture_update_from_lib/<int:lecture_id>/<int:v_file_id>', views.lecture_update_from_lib, name="lecture_update_from_lib"),
    path('sections/<int:subject_id>', views.sections, name="sections"),
    path('new_lecture_page/<int:subject_id>/<int:section_id>', views.new_lecture_page, name="new_lecture_page"),
    path('quiz_creation/<int:lecture_id>', views.quiz_creation, name="quiz_creation"),
    path('create_quiz/<int:lecture_id>', views.create_quiz, name="create_quiz"),
    path('delete_quiz_question/<int:lecture_id>/<int:question_id>', views.delete_quiz_question, name="delete_quiz_question"),
    path('edit_quiz_question/<int:lecture_id>/<int:question_id>', views.edit_quiz_question, name="edit_quiz_question"),
    path('delete_quiz/<int:lecture_id>', views.delete_quiz, name="delete_quiz"),

    path('add_text_file/<int:lecture_id>', views.add_text_file, name="add_text_file"),
    path('delete_text_file/<int:lecture_id>', views.delete_text_file, name="delete_text_file"),
    path('add_url_link/<int:lecture_id>', views.add_url_link, name="add_url_link"),
    path('delete_url_link/<int:lecture_id>', views.delete_url_link, name="delete_url_link"),
   
]
