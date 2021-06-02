from django.shortcuts import render, redirect, HttpResponseRedirect
from app_content.models import MainSubject, Transaction, Lecture, Rating
from django.contrib import messages
from .models import Review

# Create your views here.

def rating(request, subject_id):
    if request.user.is_authenticated:
        if 'rating' in request.GET:
            rating_given = request.GET['rating']
            rating_given = int(rating_given)

            subject=MainSubject.objects.get(id=subject_id)
            counter = subject.total + rating_given
            subject.total=counter
            counter_1 = subject.quantity + 1
            subject.quantity=counter_1
            subject.av_rating = subject.total / subject.quantity

            var = str(subject.av_rating / 5 * 100)
            percent = '%'
            subject.percent=var+percent
            subject.save()

            rating = Rating.objects.create(
                user=request.user,
                subject=subject,
                rating=rating_given
            )
            subject = MainSubject.objects.get(id=subject_id)
            lectures = Lecture.objects.filter(subject=subject)
            # my_courses = Transaction.objects.filter(buyer=request.user)
            context = {
                'subject': subject,
                'lectures': lectures,
                'rating' : rating
            }
            return redirect('subject_purchased', subject_id )
           
    return redirect('login')

def review(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        if request.method == 'POST':
            content = request.POST['content']
            review = Review.objects.create(
                author=request.user,
                subject=subject,
                content=content
            )
            review = Review.objects.get(subject=subject, author=request.user)
            lectures = Lecture.objects.filter(subject=subject)
            counter = subject.reviews + 1
            subject.reviews = counter
            subject.save()
            context = {
                'subject': subject,
                'lectures': lectures,
                'review': review
            }
            return redirect ('subject_purchased', subject.id)
        else:
            return render(request, 'mycourses/subject_purchased.html')
    else:
        return redirect ('login')
