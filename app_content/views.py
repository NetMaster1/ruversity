from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import MainSubject, Lecture
from django.core.paginator import Paginator
from app_reviews.models import Review

# Create your views here.


def index(request):
    subject_list = MainSubject.objects.all()
    # videos=Paginator (videos, 3)
    context = {
        # 'videos':videos,
        'subject_list': subject_list
    }
    return render(request, 'index.html', context)


def subject(request, subject_id):
            subject = MainSubject.objects.get(id=subject_id)
            lectures = Lecture.objects.filter(course=subject)

            context = {
                'subject': subject,
                'lectures': lectures
            }
            return render(request, 'subject_page.html', context)
