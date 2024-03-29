from django.contrib.auth import authenticate, login, logout
from app_content.models import MainSubject, Section, Lecture, AdditionalMaterialLink, AdditionalMaterialFile, Price, Category, Language, Transaction, Badword, Credit_card, Credit_card_type, Paypal, Main_method, Bank_account, TempImage, Question, Answer, Library, QuizQuestion, QuizAnswer
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
# Create your views here.

def admin_page (request):
    users=Group.objects.get(name='admin').user_set.all()
    if request.user in users:
        if request.method == "POST":
            id = request.POST['id']
            subject=MainSubject.objects.get(id=id)
            return redirect ('sections', subject.id)
            #return render (request, 'service/admin_page.html', context)

        else:
            return render (request, 'service/admin_page.html')
    else:
        logout(request)
        return redirect('login')

