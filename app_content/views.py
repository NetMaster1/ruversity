from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import MainSubject, Lecture, Section, Transaction, Category, Language, Keyword, Badword, Cart, DiscountOn, Library
from django.core.paginator import Paginator
from app_reviews.models import Review
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
# from django.http import HttpResponse

# Create your views here.

def index(request):
    subjects = MainSubject.objects.filter(ready='True').exclude(blocked='True').order_by('-date_posted')
    discount_time = DiscountOn.objects.get(id=1)

    if request.user.is_authenticated:
        # videos=Paginator (videos, 3)
        # Выводит последине три объекта отсортированные по дате размещения

        # bestsellers=MainSubject.objects.all().order_by('-transactions')[:4]
        # latest_subjects = MainSubject.objects.all().order_by('-date_posted')[:4]
        # highest_ranks = MainSubject.objects.all().order_by('-av_rating')[:4]

        # context = {
        #     'latest_subjects': latest_subjects,
        #     'bestsellers': bestsellers,
        #     'highest_ranks': highest_ranks
        #     }
        # return render(request, 'index.html', context)

        
        # paginator = Paginator(subjects, 12)
        # page = request.GET.get('page')
        # paged_subjects = paginator.get_page(page)

        # context = {
        #     'paged_subjects': paged_subjects,
        #     'discount_time': discount_time,
        # }
        return redirect('main_page')
    else:
        subjects = MainSubject.objects.filter(ready='True').exclude(blocked='True').order_by('-date_posted')[:20]
        paginator = Paginator(subjects, 20)
        page = request.GET.get('page')
        paged_subjects = paginator.get_page(page)

        context = {
            'discount_time': discount_time,
            'paged_subjects': paged_subjects,
        }
        return render (request, 'index.html', context)

def subject(request, subject_id):
    subject = MainSubject.objects.get(id=subject_id)
    #I don't use 'subject.length_1' directly since it comes out as '1 day 23:30:00' & I want to get rin of "day"
    subject_length=subject.length
    subject_length_hours=subject_length // 3600
    remainder=subject_length-subject_length_hours * 3600
    subject_length_min=remainder // 60
    subject_length_sec=remainder % 60
 
    lectures = Lecture.objects.filter(subject=subject, enumerator__isnull= False).order_by('enumerator')
    sections = Section.objects.filter(course=subject).order_by('enumerator')
    reviews = Review.objects.filter(subject=subject_id)
    discount_time = DiscountOn.objects.get(id=1)
    if request.user.is_authenticated:
        if Transaction.objects.filter(course=subject, buyer=request.user, payment_id__isnull=False).exists():
            transaction = Transaction.objects.get(course=subject, buyer=request.user, payment_id__isnull=False)
            if Cart.objects.filter(subject=subject, user=request.user):
                cart = Cart.objects.get(subject=subject, user=request.user)
                context = {
                    'subject': subject,
                    'subject_length_hours': subject_length_hours,
                    'subject_length_min': subject_length_min,
                    'subject_length_sec': subject_length_sec,
                    'sections': sections,
                    'lectures': lectures,
                    'reviews': reviews,
                    'cart': cart,
                    'transaction': transaction,
                    'discount_time': discount_time,
                }
                return render(request, 'subject_page.html', context)
            else:
                context = {
                    'subject': subject,
                    'subject_length_hours': subject_length_hours,
                    'subject_length_min': subject_length_min,
                    'subject_length_sec': subject_length_sec,
                    'sections': sections,
                    'lectures': lectures,
                    'reviews': reviews,
                    'transaction': transaction,
                    'discount_time': discount_time,
                }
                return render(request, 'subject_page.html', context)
        else:
            if Cart.objects.filter(subject=subject, user=request.user):
                cart = Cart.objects.get(subject=subject, user=request.user)
                context = {
                    'subject': subject,
                    'subject_length_hours': subject_length_hours,
                    'subject_length_min': subject_length_min,
                    'subject_length_sec': subject_length_sec,
                    'sections': sections,
                    'lectures': lectures,
                    'reviews': reviews,
                    'cart': cart,
                    'discount_time': discount_time,
                }
                return render(request, 'subject_page.html', context)
            else:
                context = {
                    'subject': subject,
                    'subject_length_hours': subject_length_hours,
                    'subject_length_min': subject_length_min,
                    'subject_length_sec': subject_length_sec,
                    'sections': sections,
                    'lectures': lectures,
                    'reviews': reviews,
                    'discount_time': discount_time,
                }
                return render(request, 'subject_page.html', context)
    else:
        context = {
            'subject': subject,
            'subject_length_hours': subject_length_hours,
            'subject_length_min': subject_length_min,
            'subject_length_sec': subject_length_sec,
            'sections': sections,
            'lectures': lectures,
            'reviews': reviews,
            'discount_time': discount_time,
        }
        return render(request, 'subject_page.html', context)

def gen_search(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        if keyword:  # if search line is not blank
            if MainSubject.objects.filter(title__icontains=keyword, ready='True').exclude(blocked='True').exists():
                query = MainSubject.objects.filter(title__icontains=keyword, ready='True').exclude(blocked='True').order_by('rating')
            else:
                messages.error(request, ('Курсов по вашему запросу не найдено.'))
                return redirect('main_page')

            paginator = Paginator(query, 50)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page) 

            if request.user.is_authenticated:
                keyword = Keyword.objects.create(
                    keyword=keyword,
                    user=request.user
                )
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
            query = MainSubject.objects.filter(title__icontains=keyword, ready='True').exclude(blocked='True').order_by('-rating')

            # if 'language' in request.GET:
            #     languages = request.GET.getlist('language', None)
            #     languages = Language.objects.filter(name__in=languages)
            #     query = query.filter(language__in=languages)

            #     if 'rating' in request.GET:
            #         rating = request.GET['rating']
            #         query = query.filter(av_rating__gte=rating)

            if 'sort_criteria' in request.GET:
                sort_criteria = request.GET['sort_criteria']
                if sort_criteria == 'rating':
                    query = query.order_by('rating')
                elif sort_criteria == 'reviews':
                    query = query.order_by('reviews')
                elif sort_criteria == 'transactions':
                    query = query.order_by('transactions')

            paginator = Paginator(query, 5)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged
            }
            return render(request, 'gen_search_results.html', context)

        else:
            messages.error(request, ('Данная операция доступна только зарегистрированным пользователям. Зарегистрируйтесь, пожалуйста.'))
            return redirect('login')

def main_page(request):
    # if request.user.is_authenticated:
    subjects = MainSubject.objects.filter(ready='True').exclude(blocked='True').order_by('-date_posted')
    discount_time = DiscountOn.objects.get(id=1)

    paginator = Paginator(subjects, 20)
    page = request.GET.get('page')
    paged_subjects = paginator.get_page(page)
    # ratings = Rating.objects.all()
    context = {
        'paged_subjects': paged_subjects,
        'discount_time': discount_time,
        # 'ratings': ratings,
    }
    return render(request, 'main_page.html', context)
    # else:
    #     auth.logout(request)
    #     return redirect('login')

def sorting (request, category_id):
    if request.user.is_authenticated:
        category=Category.objects.get(id=category_id)
        query = MainSubject.objects.filter(category=category_id, ready='True').exclude(blocked='True').order_by('-av_rating')
        if 'sort_criteria' in request.GET:
            sort_criteria = request.GET['sort_criteria']
            if sort_criteria == 'av_rating':
                query = query.order_by('-av_rating')
            elif sort_criteria == 'reviews':
                query = query.order_by('-reviews')
            elif sort_criteria == 'transactions':
                query = query.order_by('-transactions')

            paginator = Paginator(query, 10)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged,
                'category': category
            }
            return render(request, 'contents/list_by_category.html', context)

    else:
        return redirect ('login')

def list_software(request):
    if request.user.is_authenticated:
        category = Category.objects.get(name='Программирование и IT')
        query = MainSubject.objects.filter(category=category, ready='True').exclude(blocked='True').order_by('-av_rating')      
        if query.count()==0:
            messages.error(request, ('Курсы в данной категории отсутствуют'))
            return redirect('main_page')
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
                return render(request, 'contents/list_by_category.html', context)
            else:
                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_by_category.html', context)
        else:
            # if 'rating' in request.GET:
            #     rating = request.GET['rating']
            #     query = query.filter(av_rating__gte=rating)

            paginator = Paginator(query, 10)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged,
                'category': category
            }
            return render(request, 'contents/list_by_category.html', context)

            # else:
            #     paginator = Paginator(query, 5)
            #     page = request.GET.get('page')
            #     query_paged = paginator.get_page(page)
            #     context = {
            #         'query': query_paged
            #     }
            #     return render(request, 'contents/list_by_category.html', context)
    else:
        return redirect('login')

def list_fitness(request):
    if request.user.is_authenticated:
        category = Category.objects.get(name='Здоровье и фитнес')
        query = MainSubject.objects.filter(category=category, ready='True').exclude(blocked='True').order_by('-av_rating')
        if query.count()==0:
            messages.error(request, ('Курсы в данной категории отсутствуют'))
            return redirect('main_page') 
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
                return render(request, 'contents/list_by_category.html', context)
            else:
                paginator = Paginator(query, 5)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_by_category.html', context)
        else:
            # if 'rating' in request.GET:
            #     rating = request.GET['rating']
            #     query = query.filter(av_rating__gte=rating)

            paginator = Paginator(query, 5)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged,
                'category': category
            }
            return render(request, 'contents/list_by_category.html', context)
          
    else:
        return redirect('login')

def list_exam(request):
    category = Category.objects.get(name='Подготовка к ЕГЭ')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True').order_by('-av_rating')
    if query.count()==0:
        messages.error(request, ('Курсы в данной категории отсутствуют'))
        return redirect('main_page') 
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
                return render(request, 'contents/list_by_category.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_by_category.html', context)
        else:
           # if 'rating' in request.GET:
            #     rating = request.GET['rating']
            #     query = query.filter(av_rating__gte=rating)

            paginator = Paginator(query, 10)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged,
                'category': category
            }
            return render(request, 'contents/list_by_category.html', context)
    else:
        return redirect('login')

def list_arts(request):
    category = Category.objects.get(name='Искусство')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True').order_by('-av_rating')
    if query.count()==0:
        messages.error(request, ('Курсы в данной категории отсутствуют'))
        return redirect('main_page') 
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
                return render(request, 'contents/list_by_category.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_by_category.html', context)
        else:
           # if 'rating' in request.GET:
            #     rating = request.GET['rating']
            #     query = query.filter(av_rating__gte=rating)
            paginator = Paginator(query, 10)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged,
                'category': category
            }
            return render(request, 'contents/list_by_category.html', context)
    else:
        return redirect('login')

def list_business(request):
    category = Category.objects.get(name='Бизнес')
    query = MainSubject.objects.filter(category=category, ready='True').exclude(blocked='True').order_by('av_rating')
    if query.count()==0:
        messages.error(request, ('Курсы в данной категории отсутствуют'))
        return redirect('main_page') 
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
                return render(request, 'contents/list_by_category.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_by_category.html', context)
        else:
            # if 'rating' in request.GET:
            #     rating = request.GET['rating']
            #     query = query.filter(av_rating__gte=rating)

            paginator = Paginator(query, 10)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged,
                'category': category
            }
            return render(request, 'contents/list_by_category.html', context)
    else:
        return redirect('login')

def list_personal(request):
    category = Category.objects.get(name='Личностное развитие')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True').order_by('-av_rating')
    if query.count()==0:
        messages.error(request, ('Курсы в данной категории отсутствуют'))
        return redirect('main_page') 
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
                return render(request, 'contents/list_by_category.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_by_category.html', context)
        else:
           # if 'rating' in request.GET:
            #     rating = request.GET['rating']
            #     query = query.filter(av_rating__gte=rating)
            paginator = Paginator(query, 10)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged,
                'category': category
            }
            return render(request, 'contents/list_by_category.html', context)
    else:
        return redirect('login')

def list_languages(request):
    category = Category.objects.get(name='Языки')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True').order_by('-av_rating')
    if query.count()==0:
        messages.error(request, ('Курсы в данной категории отсутствуют'))
        return redirect('main_page') 
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
                return render(request, 'contents/list_by_category.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_by_category.html', context)
        else:
            # if 'rating' in request.GET:
            #     rating = request.GET['rating']
            #     query = query.filter(av_rating__gte=rating)
            paginator = Paginator(query, 10)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged,
                'category': category
            }
            return render(request, 'contents/list_by_category.html', context)
   
    else:
        return redirect('login')

def list_fundamental(request):
    category = Category.objects.get(name='Фундаментальные знания')
    query = MainSubject.objects.filter(
        category=category, ready='True').exclude(blocked='True').order_by('-av_rating')
    if query.count()==0:
        messages.error(request, ('Курсы в данной категории отсутствуют'))
        return redirect('main_page') 
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
                return render(request, 'contents/list_by_category.html', context)
            else:
                paginator = Paginator(query, 20)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'contents/list_by_category.html', context)
        else:
           # if 'rating' in request.GET:
            #     rating = request.GET['rating']
            #     query = query.filter(av_rating__gte=rating)
            paginator = Paginator(query, 10)
            page = request.GET.get('page')
            query_paged = paginator.get_page(page)

            context = {
                'query': query_paged,
                'category': category
            }
            return render(request, 'contents/list_by_category.html', context)
 
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
        subject = MainSubject.objects.get(id=subject_id)
        if Cart.objects.filter(user=request.user, subject=subject).exists():
            return redirect('cart')
        else:
            entry = Cart.objects.create(
                subject=subject,
                user=request.user
            )
            return redirect('cart')
    else:
        messages.error(request, ('Данная операция доступна только зарегистрированным пользователям.'))
        return redirect('login')

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        context = {
            'cart': cart
        }
        return render(request, 'contents/cart.html', context)
    else:
        messages.error(request, ('Данная операция доступна только зарегистрированным пользователям.'))
        return redirect('login')

def delete_from_cart(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        if Cart.objects.filter(user=request.user, subject=subject).exists():
            cart_item = Cart.objects.filter(user=request.user, subject=subject)
            cart_item.delete()
            return redirect('cart')
        else:
            logout(request)
            return redirect('login')
    else:
        return redirect('login')


