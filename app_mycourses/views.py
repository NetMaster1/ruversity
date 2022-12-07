from django.shortcuts import render, redirect, get_object_or_404
from app_content.models import MainSubject, Transaction, Lecture, Rating, Section, Question, Answer, QuizAnswer, QuizQuestion, QuizId
from app_reviews.models import Review
from app_mycourses.models import QuizResult
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import authenticate, login, logout
from pathlib import Path
from moviepy.editor import *
from django.core.mail import send_mail
import json, requests

# Create your views here.


def mycourses(request):
    if request.user.is_authenticated:
        my_courses = Transaction.objects.filter(buyer=request.user).order_by('-date_created')

        paginator = Paginator(my_courses, 8)
        page = request.GET.get('page')
        paged_my_courses = paginator.get_page(page)

        context = {
            'my_courses': paged_my_courses
        }
        return render(request, 'mycourses/mycourses.html', context)
    else:
        return redirect('login')

def subject_purchased(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        sections = Section.objects.filter(course=subject).order_by('enumerator')
        lectures = Lecture.objects.filter(subject=subject, enumerator__isnull= False).order_by('enumerator')
        reviews = Review.objects.filter(subject=subject_id)
        ratings = Rating.objects.filter(subject=subject_id)
        questions = Question.objects.filter(subject=subject_id)
        answers = Answer.objects.filter(subject=subject_id)
        #I don't use 'subject.length_1' directly since it comes out as '1 day 23:30:00' & I want to get rin of "day"
        subject_length=subject.length
        subject_length_hours=subject_length // 3600
        remainder=subject_length-subject_length_hours * 3600
        subject_length_min=remainder // 60
        subject_length_sec=remainder % 60

        if Transaction.objects.filter(buyer=request.user, course=subject).exists():
            if Review.objects.filter(subject=subject_id, author=request.user).exists():
                review = Review.objects.get(
                    subject=subject_id, author=request.user)
                if Rating.objects.filter(subject=subject, user=request.user).exists():
                    rating = Rating.objects.get(
                        subject=subject, user=request.user)
                    context = {
                        'subject': subject,
                        'subject_length_hours': subject_length_hours,
                        'subject_length_min': subject_length_min,
                        'subject_length_sec': subject_length_sec,
                        'rating': rating,
                        'lectures': lectures,
                        'review': review,
                        'sections': sections,
                        'reviews': reviews,
                        'ratings': ratings,
                        'questions': questions,
                        'answers': answers
                    }
                    # return render(request, 'mycourses/subject_purchased_no_stars.html', context)
                    return render(request, 'mycourses/subject_purchased.html', context)
                else:
                    context = {
                        'subject': subject,
                        'subject_length_hours': subject_length_hours,
                        'subject_length_min': subject_length_min,
                        'subject_length_sec': subject_length_sec,
                        'lectures': lectures,
                        'review': review,
                        'sections': sections,
                        'reviews': reviews,
                        'ratings': ratings,
                        'questions': questions,
                        'answers': answers
                    }
                    return render(request, 'mycourses/subject_purchased.html', context)
            else:
                if Rating.objects.filter(subject=subject, user=request.user).exists():
                    rating = Rating.objects.get(
                        subject=subject, user=request.user)
                    context = {
                        'subject': subject,
                        'subject_length_hours': subject_length_hours,
                        'subject_length_min': subject_length_min,
                        'subject_length_sec': subject_length_sec,
                        'rating': rating,
                        'lectures': lectures,
                        'sections': sections,
                        'reviews': reviews,
                        'ratings': ratings,
                        'questions': questions,
                        'answers': answers
                    }
                    # return render(request, 'mycourses/subject_purchased_no_stars.html', context)
                    return render(request, 'mycourses/subject_purchased.html', context)
                else:
                    context = {
                        'subject': subject,
                        'subject_length_hours': subject_length_hours,
                        'subject_length_min': subject_length_min,
                        'subject_length_sec': subject_length_sec,
                        'lectures': lectures,
                        'sections': sections,
                        'reviews': reviews,
                        'ratings': ratings,
                        'questions': questions,
                        'answers': answers
                    }
                    return render(request, 'mycourses/subject_purchased.html', context)
        else:
            logout(request)
            return redirect('login')

    else:
        logout(request)
        return redirect('login')

def new_question(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        if request.method == "POST":
            content = request.POST['question']
            lecture_id = request.POST['lecture']
            lecture = Lecture.objects.get(id=lecture_id)
            question = Question.objects.create(
                subject=subject,
                content=content,
                author=request.user,
                lecture=lecture,
            )
            send_mail(
                # subject
                'You have got a new question on ' + lecture.title + ' of ' + subject.title + '',
                # message
                'Please sign in your instructor account & answer the question',
                # sender
                'ruversity@gmail.com',
                # receiver
                [subject.author.email, '79200711112@yandex.ru'],
                fail_silently=False
            )
            return redirect('subject_purchased', subject_id)
    else:
        return redirect('login')

#JSON response
def quiz_api (request, lecture_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        quiz_questions=QuizQuestion.objects.filter(lecture=lecture)
        questions = []
        #dict ={}
        for quiz_question in quiz_questions:
            quiz_answers=QuizAnswer.objects.filter(question=quiz_question)
            answers = []
            for quiz_answer in quiz_answers:
                answers.append(quiz_answer.answer)
            
            questions.append({str(quiz_question.question): answers})
            #dict[quiz_question.question]=answers
            #questions.append(dict)
            #questions[quiz_question.question]=answers#ading new entry
        return JsonResponse ({
            'data': questions,
            #'time': quiz.time,
        })
        print(type(questions))
    else:
        logout(request)
        return redirect('login')

def quiz_api_page(request, lecture_id):
    lecture=Lecture.objects.get(id=lecture_id)
    context = {
        'lecture': lecture
    }
    return render (request, 'mycourses/quiz_api_page.html', context)

def open_show_quiz_page (request, lecture_id):
    quiz=QuizId.objects.create()
    lecture=Lecture.objects.get(id=lecture_id)
    questions=QuizQuestion.objects.filter(lecture=lecture)
    answers=QuizAnswer.objects.filter(lecture=lecture)
    
    context = {
        'lecture': lecture,
        'questions': questions,
        'answers': answers,
        'quiz': quiz,
    }
    return render (request, 'mycourses/show_quiz_page.html', context)

def reg_answer (request, quiz_id, lecture_id, question_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        question=QuizQuestion.objects.get(id=question_id)
        quiz=QuizId.objects.get(id=quiz_id)
        correct_answer=QuizAnswer.objects.get(question=question, correct = True)
        if request.method=='POST':
            result=QuizResult.objects.create(
                quiz=quiz,
                question=question,
                person=request.user,
                lecture=lecture
            )
            answer=request.POST['answer']
            if answer == correct_answer.answer:
                result.correct=True
                result.save()
            print(result.quiz.id)
        return redirect ('next_quiz_question', quiz.id, lecture.id)
    else:
        logout(request)
        return redirect('login')

def next_quiz_question (request, quiz_id, lecture_id):
    quiz=QuizId.objects.get(id=quiz_id)
    results=QuizResult.objects.filter(quiz=quiz)
    lecture=Lecture.objects.get(id=lecture_id)
    questions=QuizQuestion.objects.filter(lecture=lecture)
    number_of_questions=QuizQuestion.objects.filter(lecture=lecture).count()
    number_of_results=QuizResult.objects.filter(quiz=quiz).count()
    number_of_correct_results=QuizResult.objects.filter(quiz=quiz, correct=True).count()
    quality_percent=number_of_correct_results / number_of_questions * 100

    answers=QuizAnswer.objects.filter(lecture=lecture)
    questionsLeft =[]
    for question in questions:
        if not results.filter(question=question).exists():
            questionsLeft.append(question)

    context ={
        'questionsLeft': questionsLeft,
        'answers': answers,
        'quiz': quiz,
        'lecture': lecture,
        'number_of_questions': number_of_questions,
        'number_of_results': number_of_results,
        'number_of_correct_results': number_of_correct_results,
        'quality_percent': quality_percent
    }
    return render (request, 'mycourses/next_quiz_question.html', context)