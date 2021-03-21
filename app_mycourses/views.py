from django.shortcuts import render, redirect, get_object_or_404
from app_content.models import MainSubject, Transaction, Lecture, Rating
from app_reviews.models import Review
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


def mycourses(request):
    if request.user.is_authenticated:
        my_courses = Transaction.objects.filter(buyer=request.user)

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
        lectures = Lecture.objects.filter(course=subject)
        if Review.objects.filter(subject=subject_id, author=request.user).exists():
            review = Review.objects.get(subject=subject_id, author=request.user)
            if Rating.objects.filter(subject=subject, user=request.user).exists():
                rating = Rating.objects.get(subject=subject, user=request.user)
                context = {
                        'subject': subject,
                        'rating': rating,
                        'lectures': lectures,
                        'review': review
                    }
                # return render(request, 'mycourses/subject_purchased_no_stars.html', context)
                return render(request, 'mycourses/subject_purchased.html', context)
            else:
                context = {
                    'subject': subject,
                    'lectures': lectures,
                    'review': review
                }
                return render(request, 'mycourses/subject_purchased.html', context)
        else:
            if Rating.objects.filter(subject=subject, user=request.user).exists():
                rating = Rating.objects.get(subject=subject, user=request.user)
                context = {
                    'subject': subject,
                    'rating': rating,
                    'lectures': lectures,
                }
                # return render(request, 'mycourses/subject_purchased_no_stars.html', context)
                return render(request, 'mycourses/subject_purchased.html', context)
            else:
                context = {
                    'subject': subject,
                    'lectures': lectures,
                }
                return render(request, 'mycourses/subject_purchased.html', context)
    else:
        return redirect ('login')
