from django.shortcuts import render
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
