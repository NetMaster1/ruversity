from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import MainSubject, Lecture, Transaction, Category, Language, Keyword, Badword, Cart
from django.core.paginator import Paginator
from app_reviews.models import Review
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


def index(request):
    if request.user.is_authenticated:
    # videos=Paginator (videos, 3)
    #Выводит последине три объекта отсортированные по дате размещения
    
        # bestsellers=MainSubject.objects.all().order_by('-transactions')[:4]
        # latest_subjects = MainSubject.objects.all().order_by('-date_posted')[:4]
        # highest_ranks = MainSubject.objects.all().order_by('-av_rating')[:4]

        # context = {
        #     'latest_subjects': latest_subjects,
        #     'bestsellers': bestsellers,
        #     'highest_ranks': highest_ranks
        #     }
        # return render(request, 'index.html', context)

        subjects = MainSubject.objects.filter(
            ready='True').exclude(blocked='True')
        # ratings = Rating.objects.all()
        context = {
            'subjects': subjects,
            # 'ratings': ratings,
        }
        return render(request, 'main_page.html', context)
    else:
        return render(request, 'index.html')


def subject(request, subject_id):
    subject = MainSubject.objects.get(id=subject_id)
    lectures = Lecture.objects.filter(course=subject)
    reviews = Review.objects.filter(subject=subject_id)
    if request.user.is_authenticated:
        if Transaction.objects.filter(course=subject, buyer=request.user).exists():
            transaction = Transaction.objects.get(course=subject, buyer=request.user)
            context = {
                'subject': subject,
                'lectures': lectures,
                'reviews': reviews,
                'transaction': transaction,
            }
            return render(request, 'subject_page.html', context)
        else:
            if Cart.objects.filter(subject=subject, user=request.user).exists():
                cart = Cart.objects.get(subject=subject, user=request.user)
                context = {
                    'subject': subject,
                    'lectures': lectures,
                    'reviews': reviews,
                    'cart': cart
                }
                return render(request, 'subject_page.html', context)
            else:
                context = {
                      'subject': subject,
                      'lectures': lectures,
                      'reviews': reviews,
                  }
                return render(request, 'subject_page.html', context)
    else:
        context = {
            'subject': subject,
            'lectures': lectures,
            'reviews': reviews,
        }
        return render(request, 'subject_page.html', context)

def gen_search(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        if keyword:  # if search line is not blank
            # if MainSubject.objects.filter(title__icontains=keyword).exists():
            query = MainSubject.objects.filter(title__icontains=keyword, ready='True').exclude(blocked='True')

            paginator = Paginator(query, 3)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            if request.user.is_authenticated:
                keyword = Keyword.objects.create(
                    keyword=keyword,
                    user=request.user
                )

                context = {
                    'query': query_paged
                }

                template = 'gen_search_results.html'
                return render(request, template, context)
            else:
                keyword = Keyword.objects.create(
                    keyword=keyword,
                )
                context = {
                    'query': query_paged
                }
                template = 'gen_search_results.html'
                return render(request, template, context)
        else:
            return redirect('main_page')
    else:
        if request.user.is_authenticated:
            keyword = Keyword.objects.filter(user=request.user)
            query = keyword.last()
            keyword = query.keyword
            query = MainSubject.objects.filter(title__icontains=keyword, ready='True').exclude(blocked='True')
            
            if 'language' in request.GET:
                languages = request.GET.getlist('language', None)
                languages = Language.objects.filter(name__in=languages)
                query = query.filter(language__in=languages)

                if 'rating' in request.GET:
                    rating = request.GET['rating']
                    query = query.filter(av_rating__gte=rating)

                    paginator = Paginator(query, 5)
                    page = request.GET.get('page')
                    query_paged = paginator.get_page(page)

                    context = {
                            'query': query_paged
                        }
                    return render(request, 'gen_search_results.html', context)
                else:
                    paginator = Paginator(query, 5)
                    page = request.GET.get('page')
                    query_paged = paginator.get_page(page)

                    context = {
                        'query': query_paged
                    }
                    return render(request, 'gen_search_results.html', context)
            else:
                if 'rating' in request.GET:
                    rating = request.GET['rating']
                    query = query.filter(av_rating__gte=rating)

                    paginator = Paginator(query, 5)
                    page = request.GET.get('page')
                    query_paged = paginator.get_page(page)

                    context = {
                        'query': query_paged
                    }
                    return render(request, 'gen_search_results.html', context)
                else:
                    paginator = Paginator(query, 5)
                    page = request.GET.get('page')
                    query_paged = paginator.get_page(page)

                    context = {
                        'query': query_paged
                    }
                    return render(request, 'gen_search_results.html', context)
        else:
            return redirect('login')

def main_page(request):
    subjects = MainSubject.objects.filter(ready='True').exclude(blocked='True').order_by('-date_posted')

    paginator = Paginator(subjects, 8)
    page = request.GET.get('page')
    paged_subjects=paginator.get_page(page)
                
    # ratings = Rating.objects.all()
    context = {
        'subjects': paged_subjects,
        # 'ratings': ratings,
        }
    return render(request, 'main_page.html', context)

def list_software(request):
    category = Category.objects.get(name='Software & IT')
    query = MainSubject.objects.filter(category=category, ready='True').exclude(blocked='True')
    if request.user.is_authenticated:
        if 'language' in request.GET:
            languages = request.GET.getlist('language', None)
            languages = Language.objects.filter(name__in=languages)
            query = query.filter(language__in=languages)

            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                        'query': query_paged
                    }
                return render(request, 'contents/list_software.html', context)
            else:
                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_software.html', context)
        else:
            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_software.html', context)
            else:
                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)
                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_software.html', context)
    else:
        return redirect('login')


def list_fitness(request):
    category = Category.objects.get(name='Fitness')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True')
    if request.user.is_authenticated:
        if 'language' in request.GET:
            languages = request.GET.getlist('language', None)
            languages = Language.objects.filter(name__in=languages)
            query = query.filter(language__in=languages)

            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_fitness.html', context)
            else:
                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_fitness.html', context)
        else:
            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_fitness.html', context)
            else:
                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)
                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_fitness.html', context)
    else:
        return redirect('login')


def list_skills(request):
    category = Category.objects.get(name='Everyday Skills')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True')
    if request.user.is_authenticated:
        if 'language' in request.GET:
            languages = request.GET.getlist('language', None)
            languages = Language.objects.filter(name__in=languages)
            query = query.filter(language__in=languages)

            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_skills.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_skills.html', context)
        else:
            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_skills.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)
                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_skills.html', context)
    else:
        return redirect('login')


def list_arts(request):
    category = Category.objects.get(name='Arts')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True')
    if request.user.is_authenticated:
        if 'language' in request.GET:
            languages = request.GET.getlist('language', None)
            languages = Language.objects.filter(name__in=languages)
            query = query.filter(language__in=languages)

            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_arts.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_arts.html', context)
        else:
            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_arts.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)
                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_arts.html', context)
    else:
        return redirect('login')


def list_buisness(request):
    category = Category.objects.get(name='Business')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True')
    if request.user.is_authenticated:
        if 'language' in request.GET:
            languages = request.GET.getlist('language', None)
            languages = Language.objects.filter(name__in=languages)
            query = query.filter(language__in=languages)

            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_business.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_business.html', context)
        else:
            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_business.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)
                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_business.html', context)
    else:
        return redirect('login')


def list_personal(request):
    category = Category.objects.get(name='Personal Development')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True')
    if request.user.is_authenticated:
        if 'language' in request.GET:
            languages = request.GET.getlist('language', None)
            languages = Language.objects.filter(name__in=languages)
            query = query.filter(language__in=languages)

            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_personal.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_personal.html', context)
        else:
            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_personal.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)
                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_personal.html', context)
    else:
        return redirect('login')


def list_fundamental(request):
    category = Category.objects.get(name='Fundamental Science')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True')
    if request.user.is_authenticated:
        if 'language' in request.GET:
            languages = request.GET.getlist('language', None)
            languages = Language.objects.filter(name__in=languages)
            query = query.filter(language__in=languages)

            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_fundamental.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_fundamental.html', context)
        else:
            if 'rating' in request.GET:
                rating = request.GET['rating']
                query = query.filter(av_rating__gte=rating)

                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_fundamental.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)
                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_fundamental.html', context)
    else:
        return redirect('login')


def search_by_author(request, subject_author):
    subjects = MainSubject.objects.filter(ready='True').exclude(blocked='True')
    subjects = subjects.filter(author=subject_author)
    context = {
        'subjects': subjects,
    }
    return render(request, 'main_page.html', context)

def create_cart_item(request, subject_id):
    if request.user.is_authenticated:
        subject=MainSubject.objects.get(id=subject_id)
        entry = Cart.objects.create(
            subject=subject,
            user=request.user
        )
        return redirect ('cart')
    else:
        return redirect('login')

def cart(request):
   if request.user.is_authenticated:
       cart = Cart.objects.filter(user=request.user)
       context = {
           'cart': cart
       }
       return render(request, 'contents/cart.html', context)

def delete_from_cart(request, subject_id):
    if request.user.is_authenticated:
        cart_item = Cart.objects.get(id=subject_id)
        cart_item.delete()
        return redirect('cart')
    else:
        return redirect('login')
