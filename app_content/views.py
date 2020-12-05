from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import MainSubject, Lecture, Transaction, Bestseller, Rating
from django.core.paginator import Paginator
from app_reviews.models import Review

# Create your views here.


def index(request):
    # videos=Paginator (videos, 3)
    #Выводит последине три объекта отсортированные по дате размещения
    bestsellers=Bestseller.objects.all().order_by('-transactions')[:4]
    latest_subjects=MainSubject.objects.all().order_by('-date_posted')[:4]
    context = {
        'latest_subjects': latest_subjects,
        'bestsellers': bestsellers
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

def gen_search(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        if keyword:  # if search line is not blank
            if MainSubject.objects.filter(title__icontains=keyword).exists():
                query = MainSubject.objects.filter(
                    title__icontains=keyword)
                context = {
                    'query': query
                }
                template = 'gen_search_results.html'
                return render(request, template, context)
            else:
                    return render(request, 'gen_search_results.html')
        else:
            return render(request, 'gen_search_results.html')
    return render(request, 'gen_search_results.html')


def main_page(request):
    subjects = MainSubject.objects.all()
    ratings=Rating.objects.all()
    context = {
        'subjects': subjects,
        'ratings': ratings
        }
    return render(request, 'main_page.html', context)

    context = {
        # 'videos':videos,
        'subjects': subjects,   
    }
    return render (request, 'main_page.html', context)
