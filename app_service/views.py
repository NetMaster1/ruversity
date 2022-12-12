from django.contrib.auth import authenticate, login, logout
from app_content.models import MainSubject, Section, Lecture, AdditionalMaterialLink, AdditionalMaterialFile, Price, Category, Language, Transaction, Badword, Credit_card, Credit_card_type, Paypal, Main_method, Bank_account, TempImage, Question, Answer, Library, QuizQuestion, QuizAnswer
from django.shortcuts import render, redirect
# Create your views here.

def admin_page (request):
    if request.user.username == '79200711112@yandex.ru':
        if request.method == "POST":
            id = request.POST['id']
            subject=MainSubject.objects.get(id=id)
            lectures=Lecture.objects.filter(subject=subject).order_by('enumerator')
            sections=Section.objects.filter(course=subject).order_by('enumerator')
            context = {
                'subject': subject,
                'lectures': lectures,
                'sections': sections
            }
            return render (request, 'service/admin_page.html', context)

        else:
            return render (request, 'service/admin_page.html')
    else:
        logout(request)
        return redirect('login')

