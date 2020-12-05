from django.shortcuts import render, redirect, get_object_or_404
from app_content.models import MainSubject, Transaction, Lecture, Rating, AverageRating
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.


def mycourses(request):
    if request.user.is_authenticated:
        my_courses = Transaction.objects.filter(buyer=request.user)
        context = {
            'my_courses': my_courses
        }
        return render(request, 'mycourses/mycourses.html', context)
    else:
        return redirect('login')

def subject_purchased(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        if 'rating' in request.GET:
            rating = request.GET['rating']
            # rating = Rating.objects.create(
            #     user=request.user,
            #     rating=rating,
            #     subject=subject
            # )
            # rating.save()
            rating=int(rating)
            if AverageRating.objects.filter(subject=subject).exists():
                object = AverageRating.objects.get(subject=subject)
                counter = object.total + rating
                object.total = counter
                counter_1 = object.quantity + 1
                object.quantity=counter_1
                object.save()
            else:
                AverageRating.objects.create(
                    subject=subject,
                    quantity=1,
                    total=rating
                )

            my_courses = Transaction.objects.filter(buyer=request.user)
            context = {
                'my_courses': my_courses
            }
            return render(request, 'mycourses/mycourses.html', context)
        else:
            context = {
                'subject': subject,
            }
            return render(request, 'mycourses/subject_purchased.html', context)
    else:
        return redirect ('login')
