from django.shortcuts import render, redirect
from app_content.models import MainSubject, Section, Lecture, Price, Category, Language, Transaction, Badword, Credit_card, Credit_card_type, Paypal, Main_method, Bank_account, TempImage, Question, Answer
from .models import Country
from app_accounts.models import Author


from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from io import BytesIO

from django.contrib import messages
from moviepy.editor import VideoFileClip
# import moviepy
from moviepy.editor import *
import os
import cv2
import re
import PIL
from PIL import Image
from pathlib import Path
import requests
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import authenticate, login, logout

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile

from django.shortcuts import get_object_or_404
from .utils import PROCESSING_READY_TO_START, PROCESSING_FINISHED

# Create your views here.

def studio(request):
    if request.user.is_authenticated:
        if Author.objects.filter(user=request.user).exists():
            author = Author.objects.get(user=request.user)
            subjects = MainSubject.objects.filter(author=request.user.id)

            paginator = Paginator(subjects, 8)
            page = request.GET.get('page')
            subjects_paged = paginator.get_page(page)

            context = {
                'subjects': subjects_paged,
                'author': author
            }
            return render(request, 'workshop/studio.html', context)
        else:
            return render(request, 'workshop/studio.html')
    else:
        return redirect('login')

def create_author_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            background = request.POST['background']
            photo = request.FILES['photo']
            if photo.name.endswith('.jpg') or photo.name.endswith('.png') or photo.name.endswith('.gif') or photo.name.endswith('.bmp') or photo.name.endswith('.jpeg'):
                if re.search(r'[а-яА-я]', photo.name) == None:
                    author = Author.objects.create(
                        background=background,
                        photo=photo,
                        user=request.user,
                        first_name=request.user.first_name,
                        last_name=request.user.last_name
                    )
                    img = cv2.imread(author.photo.path, 0)
                    print(type(img))
                    wid = img.shape[1]
                    hgt = img.shape[0]
                    ratio = wid / hgt
                    if ratio < 0.9 or ratio > 1.1:
                        author.delete()
                        #messages.error(request, 'Image has inproper ratio. Use a square photo with aspect ratio of 1.')
                        messages.error(request, 'Неправильное соотношение сторон фото. Загрузите фото с соотношением сторон 1х1;')
                        return redirect('studio')

                    else:
                        author = Author.objects.get(user=request.user)
                        context = {
                            'author': author
                        }
                        return redirect('studio')
                else:
                    messages.error(request, 'Используйте латинницу в названии файла')
                    return redirect('studio')
            else:
                messages.error(request, 'Вы загрузили файл неправильного формата. Загрузите файл в формате jpg, jpeg, png или bmp')
                # messages.error(request, 'File has inproper format. Load jpg, jpeg, png or bmp file')
                return redirect('studio')
        else:
            return redirect('studio')
    else:
        return redirect('login')

def author_page(request, user_id):
        if Author.objects.filter(user=user_id).exists():
            author = Author.objects.get(user=user_id)
            subjects =MainSubject.objects.filter(author=author.user)
            context = {
                'author': author,
                'subjects': subjects
            }
            return render(request, 'workshop/author_page.html', context)
        else:
            messages.error(
                request, 'The author has no profile yet')
            return redirect('studio')

def edit_author_page(request, user_id):
    if request.user.is_authenticated:
        author = Author.objects.get(user=user_id)
        if author.user == request.user:
            if request.method == 'POST':
                background = request.POST['background']
                photo = request.FILES['photo']

                if photo.name.endswith('.jpg') or photo.name.endswith('.png') or photo.name.endswith('.gif') or photo.name.endswith('.bmp') or photo.name.endswith('.jpeg'):
                    if re.search(r'[а-яА-я]', photo.name) == None:
                        temp_image = TempImage.objects.create(temp_thumbnail_file=photo)
                        img = cv2.imread(temp_image.temp_thumbnail_file.path, 0)

                        wid = img.shape[1]
                        hgt = img.shape[0]
                        ratio = wid / hgt
                        if ratio < 0.9 or ratio > 1.1:
                            temp_image.delete()
                            messages.error(request,  'Неправильное соотношение сторон фото. Загрузите фото с соотношением сторон 1х1;')
                            return redirect('author_page', user_id)
                        else:
                            author.background = background
                            author.photo = photo
                            author.save()
                            return redirect('author_page', user_id)
                    else:
                       messages.error(request, 'Используйте латинницу в названии файла')
                       return redirect('author_page', user_id)
                else:
                    messages.error(request, 'Вы загрузили файл неправильного формата. Загрузите файл в формате jpg, jpeg, png или bmp')
                    return redirect('author_page', user_id)

            return redirect('author_page', user_id)
        else:
            logout(request)
            return redirect('login')
    else:
        return redirect('login')

def create_new_subject(request):
    if request.user.is_authenticated:
        languages = Language.objects.all()
        categories = Category.objects.all()
        context = {
            'languages': languages,
            'categories': categories
        }
        if request.method == 'POST':
            title = request.POST['title']
            category_id = request.POST['category']
            language_id = request.POST['language']
            description = request.POST['description']
            prerequisite = request.POST['prerequisite']
            thumbnail = request.FILES['thumbnail_file']
            lang_fkey = Language.objects.get(id=language_id)
            categ_fkey=Category.objects.get(id=category_id)
            author = request.user
            price = Price.objects.get(id=1)
            if thumbnail.name.endswith('.jpg') or thumbnail.name.endswith('.png') or thumbnail.name.endswith('.gif') or thumbnail.name.endswith('.bmp') or thumbnail.name.endswith('.jpeg'):
                new_subject = MainSubject.objects.create(
                    title=title,
                    thumbnail_file=thumbnail,
                    author=author,
                    price=price,
                    description=description,
                    prerequisite=prerequisite,
                    category=categ_fkey,
                    language=lang_fkey
                )

                img = cv2.imread(new_subject.thumbnail_file.path, 0)
                wid = img.shape[1]
                hgt = img.shape[0]
                ratio = wid / hgt
                if ratio < 1.5 or ratio > 1.8:
                    new_subject.delete()
                    messages.error(request, 'Image has inproper ratio. Use ration of 1.7 .')
                    return redirect('create_new_subject')

                else:
                    my_subjects = MainSubject.objects.filter(author=request.user)
                    context = {
                    'my_subjects': my_subjects
                    }
                    return redirect('studio')
            else:
                messages.error(request, 'File has inproper format. Load jpg, jpeg, png or bmp file')
                return redirect('create_new_subject')

        else:
            return render(request, 'workshop/create_new_subject.html', context)
    else:
        logout(request)
        return redirect('login')

def edit_subject(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        if subject.ready == False:
            if request.user == subject.author:
                if request.method == "POST":
                    subject.title = request.POST['title']
                    language_id = request.POST['language']
                    language = Language.objects.get(id=language_id)
                    subject.language=language
                    category_id = request.POST['category']
                    category = Category.objects.get(id=category_id)
                    subject.category=category
                    subject.description = request.POST['description']
                    subject.prerequisite = request.POST['prerequisites']
                    thumbnail = request.FILES['thumbnail']
                    if thumbnail.name.endswith('.jpg') or thumbnail.name.endswith('.png') or thumbnail.name.endswith('.gif') or thumbnail.name.endswith('.bmp') or thumbnail.name.endswith('.jpeg'):
                        temp_image=TempImage.objects.create(temp_thumbnail_file=thumbnail)
                        img = cv2.imread(temp_image.temp_thumbnail_file.path, 0)
                        wid = img.shape[1]
                        hgt = img.shape[0]
                        ratio = wid / hgt
                        if ratio < 1.5 or ratio > 1.8:
                            messages.error(request, 'Image has inproper ratio. Use ration of 1.7 .')
                            temp_image.delete()
                            return redirect('edit_subject', subject_id)

                        else:
                            subject.thumbnail_file = thumbnail
                            subject.save()
                            languages = Language.objects.all()
                            categories = Category.objects.all()

                            context = {
                                'subject': subject,
                                # 'sections': sections,
                                # 'lectures': lectures,
                                'languages': languages,
                                'categories': categories
                            }
                            return render(request, 'workshop/edit_subject.html', context)
                    else:
                        messages.error(request, 'File has inproper format. Load jpg, jpeg, png or bmp file')
                        return redirect('edit_subject', subject_id)
                else:
                    if Section.objects.filter(course=subject).exists():
                        sections = Section.objects.filter(course=subject)
                        if Lecture.objects.filter(subject=subject).exists:
                            lectures=Lecture.objects.filter(subject=subject)
                            languages = Language.objects.all()
                            categories = Category.objects.all()
                            context = {
                                'subject': subject,
                                'sections': sections,
                                'lectures': lectures,
                                'languages': languages,
                                'categories': categories
                                }
                            # return redirect('studio')
                            return render(request, 'workshop/edit_subject.html', context)
                        else:
                            languages = Language.objects.all()
                            categories = Category.objects.all()
                            context = {
                            'subject': subject,
                            'languages': languages,
                            'categories': categories
                        }
                        return render(request, 'workshop/edit_subject.html', context)
                    else:
                        languages = Language.objects.all()
                        categories = Category.objects.all()
                        context = {
                            'subject': subject,
                            'languages': languages,
                            'categories': categories
                        }
                        return render(request, 'workshop/edit_subject.html', context)
            else:
                logout(request)
                return redirect('login')
        else:
            if request.method == "POST":
                if Question.objects.filter(subject=subject).exists():
                    questions=Question.objects.filter(subject=subject)
                    answers=Answer.objects.filter(subject=subject)
                    context = {
                            'questions': questions,
                            'subject': subject,
                            'answers': answers
                        }
                    return render (request, 'workshop/edit_subject.html', context)
                else:
                    return render(request, 'workshop/edit_subject.html')
            else:
                questions = Question.objects.filter(subject=subject)
                answers=Answer.objects.filter(subject=subject)
                context = {
                            'questions': questions,
                            'answers': answers,
                            'subject': subject
                        }
                return render (request, 'workshop/edit_subject.html', context)
    else:
        return redirect('login')

def delete_subject(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        if request.user == subject.author:
            if subject.ready == True:
                messages.error(request, 'Sorry, you can not delete a loaded subject.')
                return redirect('edit_subject', subject_id)
            else:
                subject.delete()
                return redirect('studio')
        else:
            logout(request)
            return redirect('login')
    else:
        logout(request)
        return redirect('login')

def create_new_section(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        if request.user == subject.author:
            if request.method == 'POST':
                title = request.POST['title']
                section = Section.objects.create(
                    title=title,
                    course=subject
                )
                return redirect ('edit_subject', subject_id)
            else:
                return redirect('edit_subject', subject_id)
        logout(request)
        return redirect('login')
    return redirect('login')

def edit_section (request, subject_id, section_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        section=Section.objects.get(id=section_id)
        if request.user == subject.author:
            if request.method == 'POST':
                title = request.POST['title']
                section.title = title
                section.save()
                return redirect('edit_section', subject_id, section_id)
            else:
                section = Section.objects.get(id=section_id)
                lectures=Lecture.objects.filter(section=section)
                context = {
                    'subject': subject,
                    'section': section,
                    'lectures': lectures,
                }
                return render(request, 'workshop/edit_section.html', context)
        else:
            logout(request)
            return redirect('login')
    return redirect('login')

def delete_section (request, subject_id, section_id):
    if request.user.is_authenticated:
        subject=MainSubject.objects.get(id=subject_id)
        if request.user == subject.author:
            section = Section.objects.get(id=section_id)
            section.delete()
            return redirect ('edit_subject', subject_id)
        else:
            logout(request)
            return redirect('login')
    else:
        return redirect('login')

def create_new_lecture(request, subject_id, section_id):
    #
    # Initial sanity checks
    #

    if not request.user.is_authenticated:
        return redirect('login')

    subject=MainSubject.objects.get(id=subject_id)
    section = Section.objects.get(id=section_id)

    if request.user != subject.author:
        logout(request)
        return redirect('login')

    if request.method != 'POST':
        return redirect('edit_section', subject_id, section_id)

    #
    # Request parameters check
    #

    video_file = request.FILES['video_file']
    video_file_name = video_file.file.name
    title = request.POST['title']
    subtitle_file = request.POST.get('subtitle_file', False)
    # translation_file = request.FILES['translation_file']
    author = request.user
    free_access = False
    try:
        if request.POST['free_access']:
            free_access = True
    except KeyError:
        free_access = False

    if not video_file_name.endswith('.mp4'):
        messages.error(request, 'File has inproper format. Load mp4 file')
        return redirect('edit_section', subject_id, section_id)

    size_bytes = os.path.getsize(video_file_name)
    size_mbytes = size_bytes/1024/1024
    if size_mbytes > 100:
        messages.error(request, 'Your file is too large.')
        return redirect('edit_section', subject_id, section_id)

    clip = VideoFileClip(video_file_name)
    length = clip.duration / 60
    size_mb = size_mbytes

    lecture = Lecture.objects.create(
        title=title,
        video_file=video_file,
        subtitle_file=subtitle_file,
        # translation_file=translation_file,
        author=author,
        section=section,
        subject=subject,
        free=free_access,
        length=length,
        size_mb=size_mb
    )

    lectures = Lecture.objects.filter(subject=subject)
    lectures = lectures.filter(section=section)
    context = {
        'subject': subject,
        'section': section,
        'lectures': lectures,
    }
    return redirect('edit_section', subject_id, section_id)

def edit_lecture(request, lecture_id):
    if request.user.is_authenticated:
        lecture = Lecture.objects.get(id=lecture_id)
        subject = lecture.subject
        section = lecture.section
        if request.user == subject.author:
            if subject.ready == True:
                messages.error(request, 'Sorry, you can not edit a loaded lecture.')
                return redirect('edit_section', subject.id, section.id)
            else:
                if request.method == "POST":
                    title = request.POST['title']
                    video_file = request.FILES['video_file']
                    subtitle_file = request.FILES['subtitle_file']
                    # translation_file = request.FILES['translation_file']
                    if video_file.name.endswith('.mp4'):
                        lecture.video_file=video_file
                        lecture.title = request.POST['title']
                        lecture.save()
                        path = lecture.video_file.path
                        size_bytes = os.path.getsize(path)
                        size_mbytes = size_bytes / 1024 / 1024
                        lecture.size_mbytes = size_mbytes
                        lecture.save()
                        if lecture.size_mb > 100:
                            lecture.delete()
                            messages.error(request, 'Your file is too large.')
                            return redirect('edit_section', subject.id, section.id)
                        else:
                            lectures = Lecture.objects.filter(subject=subject)
                            context = {
                                'lectures': lectures,
                                'section': section,
                                'subject': subject
                            }
                            return redirect('edit_section', subject.id, section.id)
                    else:
                        messages.error(request, 'File has inproper format. Load mp4 file')
                        return redirect('edit_section', subject.id, section.id)
                else:
                    return redirect('edit_section', subject.id, section.id)
        else:
            logout(request)
            return redirect('login')
    else:
        logout(request)
        return redirect('login')

def delete_lecture(request, lecture_id):
    if request.user.is_authenticated:
        lecture = Lecture.objects.get(id=lecture_id)
        subject = lecture.subject
        section=lecture.section
        if request.user == subject.author:
            if subject.ready == True:
                messages.error(request, 'Sorry, you can not delete a loaded lecture.')
                return redirect('edit_section', subject_id, section_id)
            else:
                lecture.delete()
                lectures = Lecture.objects.filter(subject=subject)
                return redirect('edit_section', subject.id, section.id)
        else:
            logout(request)
            return redirect('login')
    else:
        logout(request)
        return redirect('login')

def video(request, subject_id, lecture_id):
    if not request.user.is_authenticated:
        return redirect('login')

    subject = get_object_or_404(MainSubject, id=subject_id)
    the_video = get_object_or_404(Lecture, id=lecture_id)

    if not (Transaction.objects.filter(buyer=request.user, course=subject).exists()
            or request.user == subject.author
            or the_video.free == True):
        logout(request)
        messages.error(request, 'Для просмотра видео вам необходимо приобрести данный курс.')
        return redirect('login')

    context = {'the_video': the_video}
    template_name = 'video.html'
    if the_video.processing_state != PROCESSING_FINISHED:
        template_name = 'video_is_being_processed.html'

    return render(request, template_name, context)

def agreement(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        context = {
            'subject': subject,
        }
        return render(request, 'workshop/agreement.html', context)
    else:
        return redirect ('login')

def disagree(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        lectures = Lecture.objects.filter(subject=subject)
        context = {
            'subject': subject,
            'lectures': lectures
        }
        return render(request, 'workshop/edit_subject.html', context)
    else:
        return redirect ('login')

#saving subject & section length in min & checking for badwords
def agree(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        if Lecture.objects.filter(subject=subject.id).exists():
            badwords=Badword.objects.all()
            lectures = Lecture.objects.filter(subject=subject)
            subject_duration=0
            for lecture in lectures:
                subject_duration += lecture.length
            subject.length = subject_duration
            subject.save()
            sections = Section.objects.filter(course=subject)
            for section in sections:
                lectures_sec=lectures.filter(section=section)
                section_length=0
                for lecture_sec in lectures_sec:
                    section_length += lecture_sec.length
                section.length=section_length
                section.save()
            if badwords:
                for word in badwords:
                    if word.badword in subject.title:
                        subject.blocked = True
                        subject.save()
                    else:
                        subject.checked = True
                        subject.ready=True
                        subject.save()
            else:
                subject.checked = True
                subject.ready=True
                subject.save()
            for lecture in lectures:
                lecture.processing_state = PROCESSING_READY_TO_START
                lecture.save()
                if badwords:
                    for word in badwords:
                        if word.badword in lecture.title:
                            lecture.blocked = True
                            lecture.save()
                            subject.blocked = True
                            subject.save()
            return redirect('main_page')
        else:
            subject_id=subject.id
            messages.error(request, 'В курсе отсутствуют лекции. Пожалуйста, создайте лекции.')
            return redirect('edit_subject', subject_id)
    else:
        return redirect('login')

def author_profile(request):
    if request.user.is_authenticated:
        countries=Country.objects.all()
        if Group.objects.filter(name='entity').exists():
            group = Group.objects.get(name='entity').user_set.all()

            if Main_method.objects.filter(user=request.user).exists():
                main_method = Main_method.objects.get(user=request.user)
                if main_method.method == 'paypal':
                    if Paypal.objects.filter(user=request.user).exists():
                        method = Paypal.objects.get(user=request.user)
                    else:
                        return render(request, 'workshop/author_profile.html')
                elif main_method.method == 'credit_card':
                    if Credit_card.objects.filter(user=request.user).exists():
                        method = Credit_card.objects.get(user=request.user)
                    else:
                        credit_card_types = Credit_card_type.objects.all()
                        context = {
                            'credit_card_types': credit_card_types
                        }
                        return render(request, 'workshop/author_profile.html', context)
                elif main_method.method == 'bank_account':
                    if Bank_account.objects.filter(user=request.user).exists():
                        method = Bank_account.objects.get(user=request.user)
                    else:
                        return render(request, 'workshop/author_profile.html')

                context = {
                        'group': group,
                        'main_method': main_method,
                        'method': method,
                        'countries': countries,
                        # 'credit_card_types': credit_card_types
                    }
                return render(request, 'workshop/author_profile.html', context)
            else:
                credit_card_types = Credit_card_type.objects.all()
                countries=Country.objects.all()
                context = {
                    'credit_card_types': credit_card_types,
                    'countries': countries
                }
                return render(request, 'workshop/author_profile.html', context)
        else:
            if Main_method.objects.filter(user=request.user).exists():
                main_method = Main_method.objects.get(user=request.user)
                if main_method.method == 'paypal':
                    if Paypal.objects.filter(user=request.user).exists():
                        method = Paypal.objects.get(user=request.user)
                elif main_method.method == 'credit_card':
                    if Credit_card.objects.filter(user=request.user).exists():
                        method = Credit_card.objects.get(user=request.user)
                context = {
                    'main_method': main_method,
                    'method': method
                }
                return render(request, 'workshop/author_profile.html', context)
            else:
                credit_card_types = Credit_card_type.objects.all()
                context = {
                    'credit_card_types': credit_card_types,
                }
                return render(request, 'workshop/author_profile.html', context)
    else:
        return redirect('login')

def main_method(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if Main_method.objects.filter(user=request.user).exists():  #fool protection
                main_method = Main_method.objects.get(user=request.user)
                return redirect('author_profile')
            else:
                method = request.POST['method']
                main_method = Main_method.objects.create(
                    user=request.user,
                    method=method
                )
                if method == 'paypal':
                    name = request.POST['name']
                    method = Paypal.objects.create(
                        user=request.user,
                        name=name
                    )
                elif method == 'credit_card':
                    first_name = request.POST['first_name']
                    last_name = request.POST['last_name']
                    card_number = request.POST['card_number']
                    credit_card_type = request.POST['credit_card_type']
                    method = Credit_card.objects.create(
                            user=request.user,
                            first_name=first_name,
                            last_name=last_name,
                            card_number=card_number,
                            card_type=credit_card_type
                        )
                elif method == 'bank_account':
                    country = request.POST['country']
                    entity_name = request.POST['entity_name']
                    itin = request.POST['itin']
                    bic = request.POST['bic']
                    bank_account = request.POST['bank_account']
                    account = request.POST['account']
                    method = Bank_account.objects.create(
                            user=request.user,
                            country=country,
                            entity_name=entity_name,
                            itin=itin,
                            bin=bic,
                            bank_account=bank_account,
                            account=account
                        )
                context = {
                    'main_method': main_method,
                    'method': method
                    }
                return redirect('author_profile')


    else:
        return redirect('login')

def edit_main_method(request):
    if request.user.is_authenticated:
        main_method = Main_method.objects.get(user=request.user)
        if main_method.method == 'paypal':
            if Paypal.objects.filter(user=request.user).exists():
                method = Paypal.objects.get(user=request.user).delete()
            else:
                return redirect ('author_profile')
        elif main_method.method == 'credit_card':
            if Credit_card.objects.filter(user=request.user).exists():
                method = Credit_card.objects.get(user=request.user).delete()
            else:
                return redirect('author_profile')

        elif main_method.method == 'bank_account':
            if Bank_account.objects.filter(user=request.user).exists():
                method = Bank_account.objects.get(user=request.user).delete()
            else:
                return redirect('author_profile')
        main_method.delete()
        return redirect('author_profile')
    else:
        return redirect('login')

def credit_card(request):
    if request.user.is_authenticated:
        if Credit_card.objects.filter(user=request.user).exists():#security reasons
            return redirect('author_profile')
        else:
            if request.method == "POST":
                if Main_method.objects.filter(user=request.user).exists(): #security reasons
                    first_name = request.POST['first_name']
                    last_name = request.POST['last_name']
                    card_number = request.POST['card_number']
                    credit_card_type = request.POST['credit_card_type']
                    method = Credit_card.objects.create(
                        user=request.user,
                        first_name=first_name,
                        last_name=last_name,
                        card_number=card_number,
                        card_type=credit_card_type
                    )
                    # main_method = Main_method.objects.get(user=request.user)
                    # context = {
                    #     'method': method,
                    #     'main_method': main_method,
                    # }
                    return redirect ('author_profile')
                else:
                    return redirect ('author_profile')
            else:
                credit_card_types=Credit_card_type.objects.all()
                context = {
                    'credit_card_types': credit_card_types,
                }
                return render(request, 'workshop/credit_card.html', context)
    else:
        return redirect('login')

def paypal(request):
    if request.user.is_authenticated:
        if Paypal.objects.filter(user=request.user).exists():   #sercurity reasons
            return redirect('author_profile')
        else:
            if request.method == "POST":
                if Main_method.objects.filter(user=request.user).exists():#security reasons
                    name = request.POST['name']
                    method = Paypal.objects.create(
                        user=request.user,
                        name=name
                    )
                    main_method = Main_method.objects.get(user=request.user)
                    context = {
                        'method': method,
                        'main_method': main_method
                    }
                    # return render(request, 'workshop/author_profile.html', context)
                    return redirect ('author_profile')
                else:
                    return redirect('author_profile')
            else:
                return render(request, 'workshop/paypal.html')
    else:
        return redirect('login')

def bank_account(request):
    pass

def transactions(request):
    if request.user.is_authenticated:
        my_subjects = MainSubject.objects.filter(author=request.user)
        my_transactions = Transaction.objects.filter(course__in=my_subjects)
        if 'sort' in request.GET:
            option = request.GET['sort']
            if option == 'title':
                my_transactions=my_transactions.order_by('course')
            elif option == 'buyer':
                my_transactions=my_transactions.order_by('buyer')
            elif option == 'date':
                my_transactions=my_transactions.order_by('date_bought')
            context = {
                    'my_transactions': my_transactions
                }
            return render(request, 'workshop/transactions.html', context)
        else:
            context = {
                            'my_transactions': my_transactions
                        }
            return render(request, 'workshop/transactions.html', context)
    return redirect('login')

class GeneratePDF(View):
    # def get(self, request, *args, **kwargs):
    def get(self, request):
        data = {
            # 'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('workshop/transactions_pdf.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        return response
        # return HttpResponse(result.getvalue(), content_type='application/pdf')
        # return None

def answer(request, subject_id, question_id):
    if request.user.is_authenticated:
        subject= MainSubject.objects.get(id=subject_id)
        question=Question.objects.get(id=question_id)
        if request.method == "POST":
            content = request.POST['answer']
            answer = Answer.objects.create(
                subject=subject,
                question=question,
                content=content,
                author=request.user
            )
            return redirect('edit_subject', subject_id)
    else:
        return redirect('login')

