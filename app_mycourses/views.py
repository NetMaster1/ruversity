from django.shortcuts import render, redirect, get_object_or_404
from app_content.models import MainSubject, Transaction, Lecture
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
