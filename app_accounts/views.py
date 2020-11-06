from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            messages.success(request, ('You have registered'))
            return redirect('dashboard')
    else:
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)

# function is called login_user to differentiate it from module 'login' imported above


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, ('Your have successfully been logged in'))
            return redirect('dashboard')
        else:
            messages.success(
                request, ('Incorrect username or password. Check your credentials & try again'))
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('You are now logged out'))
    return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/dashboard.html')
    else:
        return redirect('login')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            new_password = request.POST['new_password']
            user = User.objects.get(id=request.user)
            user.set_password(new_password)
            user.save
            return redirect('dashboard')
    else:
        return redirect('dashboard')
