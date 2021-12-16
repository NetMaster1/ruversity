from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Create your views here.


def contacts(request):
    return render(request, 'contacts/contacts.html')

def help(request):
    return render(request, 'contacts/help.html')

def termsofuse(request):
    return render(request, 'contacts/termsofuse.html')

def partnership(request):
    return render(request, 'contacts/partnership.html')

def socialmedia(request):
    return render(request, 'contacts/socialmedia.html')

def career(request):
    return render(request, 'contacts/career.html')

def email (request):
    if request.user.is_authenticated:
        if request.method == "POST":
            message = request.POST['message']
            title = request.POST['title']
            send_mail(
              #subject
              title,
              #message
              message,
              #sender
              request.user.email,
              #receiver
              ['ruversity@gmail.com'],
              fail_silently=False
            )
            messages.success(request, 'You successfully sent us your message.')
            return redirect ('email')
        else:
            return render(request, 'contacts/email.html')
    else:
        return redirect('login')
