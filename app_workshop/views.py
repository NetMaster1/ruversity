from contextlib import nullcontext
from django.forms import NullBooleanField
from django.shortcuts import render, redirect
from app_content.models import MainSubject, Section, Lecture, AdditionalMaterialLink, AdditionalMaterialFile, Price, Category, Language, Transaction, Badword, Credit_card, Credit_card_type, Paypal, Main_method, Bank_account, TempImage, Question, Answer, Library, QuizQuestion, QuizAnswer
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

import datetime
# Create your views here.

def studio(request):
    if request.user.is_authenticated:
        if Author.objects.filter(user=request.user).exists():
            author = Author.objects.get(user=request.user)
            subjects = MainSubject.objects.filter(author=request.user.id)

            # paginator = Paginator(subjects, 8)
            # page = request.GET.get('page')
            # subjects_paged = paginator.get_page(page)

            context = {
                'subjects': subjects,
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
            # if re.search(r'[а-яА-я]', photo.name) == None:
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
                    return render (request, 'workshop/author_page.html', context)
                # else:
                #     messages.error(request, 'Используйте латинницу в названии файла')
                #     return redirect('studio')
            else:
                messages.error(request, 'Вы загрузили файл неправильного формата. Загрузите файл в формате jpg, jpeg, png или bmp')
                # messages.error(request, 'File has inproper format. Load jpg, jpeg, png or bmp file')
                return redirect('studio')
    else:
        return redirect('login')

def author_page(request, user_id):
        if Author.objects.filter(user=user_id).exists():
            author = Author.objects.get(user=user_id)
            subjects =MainSubject.objects.filter(author=author.user, ready=True, blocked=False)
            context = {
                'author': author,
                'subjects': subjects
            }
            return render(request, 'workshop/author_page.html', context)
        else:
            messages.error (request, 'Профиль автора отсутствует. Создайте его.')
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
        logout(request)
        return redirect('login')

#=================================Subject Operations===================================
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
            thumbnail_file = request.FILES['thumbnail_file']
            lang_fkey = Language.objects.get(id=language_id)
            categ_fkey=Category.objects.get(id=category_id)
            author = request.user
            author_price = request.POST['author_price']
            price = Price.objects.get(id=1)
            if thumbnail_file.name.endswith('.jpg') or thumbnail_file.name.endswith('.png') or thumbnail_file.name.endswith('.gif') or thumbnail_file.name.endswith('.bmp') or thumbnail_file.name.endswith('.jpeg'):
                new_subject = MainSubject.objects.create(
                    title=title,
                    thumbnail_file=thumbnail_file,
                    author=author,
                    price=price,
                    description=description,
                    prerequisite=prerequisite,
                    category=categ_fkey,
                    language=lang_fkey,
                    author_price=author_price,
                )
                img = cv2.imread(new_subject.thumbnail_file.path, 0)
                wid = img.shape[1]
                hgt = img.shape[0]
                ratio = wid / hgt
                if ratio < 1.5 or ratio > 1.8:
                    new_subject.delete()
                    messages.error(request, 'Некорректное соотношение сторон. Используйте отношение длины изображения к его высоте равное 1.7.')
                    # messages.error(request, 'Image has inproper ratio. Use ration of 1.7 .')
                    return redirect('create_new_subject')
                else:
                    try:
                        if request.POST['dicount_program']:
                            discount_program = True
                    except KeyError:
                        discount_program = False
                    new_subject.discount_program = discount_program
                    new_subject.save()
                    my_subjects = MainSubject.objects.filter(author=request.user)
                    context = {
                    'my_subjects': my_subjects
                    }
                    return redirect('studio')
            else:
                # messages.error(request, 'File has inproper format. Load jpg, jpeg, png or bmp file')
                messages.error(request, 'Некорректный формат файла. Используйте файл в формате jpg, jpeg, png или bmp.')
                return redirect('create_new_subject')

        else:
            return render(request, 'workshop/create_new_subject.html', context)
    else:
        logout(request)
        return redirect('login')

def edit_subject(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        users=Group.objects.get(name='admin').user_set.all()
        if subject.ready == False:
            if request.user != subject.author and request.user not in users:
                logout(request)
                return redirect('login')
            if request.method == "POST":
                title = request.POST.get('title')
                if title:
                    subject.title=title
                language_id = request.POST.get('language')
                if language_id:
                    language = Language.objects.get(id=language_id)
                    subject.language=language
                category_id = request.POST.get('category')
                if category_id:
                    category = Category.objects.get(id=category_id)
                    subject.category=category
                description = request.POST.get('description')
                if description:
                    subject.description=description
                    description = request.POST.get('description')
                prerequisites = request.POST.get('prerequisites')
                if prerequisites:
                    subject.prerequisite=prerequisites
                author_price = request.FILES.get('author_price')
                if author_price:
                    subject.author_price=author_price
                additional_file = request.FILES.get('thumbnail')
                if additional_file:
                    if additional_file.name.endswith('.jpg') or additional_file.name.endswith('.png') or additional_file.name.endswith('.gif') or additional_file.name.endswith('.bmp') or additional_file.name.endswith('.jpeg'):
                        temp_image=TempImage.objects.create(temp_thumbnail_file=additional_file)
                        img = cv2.imread(temp_image.temp_thumbnail_file.path, 0)
                        wid = img.shape[1]
                        hgt = img.shape[0]
                        ratio = wid / hgt
                        if ratio < 1.5 or ratio > 1.8:
                            # messages.error(request, 'Image has inproper ratio. Use ration of 1.7 .')
                            messages.error(request, 'Некорректное соотношение сторон. Используйте отношение длины изображения к его высоте равное 1.7.')
                            temp_image.delete()
                            return redirect('edit_subject', subject_id)
                        else:
                            subject.thumbnail_file = additional_file
                    else:
                        messages.error(request, 'Некорректный формат файла. Загрузите файл в формате jpg, jpeg, png или bmp')
                        return redirect('edit_subject', subject_id)

                try:
                    if request.POST['discount_program']:
                        discount_program = True
                except KeyError:
                    discount_program = False
                subject.discount_programs = discount_program
                subject.save()
                return redirect ('edit_subject', subject.id )
            else:
                if Library.objects.filter(subject=subject).exists():
                    v_files=Library.objects.filter(subject=subject)
                    languages = Language.objects.all()
                    categories = Category.objects.all()
                    context = {
                        'v_files': v_files,
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
            if request.user in users:
                messages.error(request, 'Вы вошли как админ для редактирования курса.')

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
                messages.error(request, 'Вы не можете удалить загруженный курс.')
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

#===============================Sections======================================

def create_new_section(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == 'POST':
            title = request.POST['title']
            #enumerator = request.POST['enumerator']
            if Section.objects.filter(course=subject).exists():
                numberOfSections=Section.objects.filter(course=subject).count()
            else:
                numberOfSections=0
                
            section = Section.objects.create(
                title=title,
                course=subject,
                enumerator=numberOfSections + 1
            )
            return redirect ('sections', subject.id)          
    else:
        logout(request)
        return redirect('login')

def sections (request, subject_id):
    if request.user.is_authenticated:
        subject=MainSubject.objects.get(id=subject_id)
        sections=Section.objects.filter(course=subject).order_by('enumerator')
        lectures=Lecture.objects.filter(subject=subject).order_by('enumerator')
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.user != subject.author and request.user in users:
            messages.error(request, 'Вы вошли как админ для редактирования курса.')
        context = {
            'subject': subject,
            'sections': sections,
            'lectures': lectures,
            'users': users,
        }
        return render(request, 'workshop/sections.html', context)
    else:
        logout(request)
        return redirect('login')

def edit_section_title (request, section_id):
    if request.user.is_authenticated:
        section=Section.objects.get(id=section_id)
        subject=section.course
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.user != subject.author and request.user in users:
            messages.error(request, 'Вы вошли как админ для редактирования курса.')
        if request.method == 'POST':
            title = request.POST['title']
            section.title = title
            section.save()
            return redirect('sections', subject.id)
        else:
            context ={
                'section': section,
                'subject': subject,
            }
            return render (request, 'workshop/section_title_edit_page.html', context )
    else:
        logout(request)
        return redirect('login')

def delete_section (request, subject_id, section_id):
    if request.user.is_authenticated:
        subject=MainSubject.objects.get(id=subject_id)
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        section = Section.objects.get(id=section_id)
        section.delete()
        return redirect ('sections', subject_id)

    else:
        return redirect('login')

#===================================Lectures Operations=============================
def new_lecture_page (request, subject_id, section_id):
    if request.user.is_authenticated:
        subject=MainSubject.objects.get(id=subject_id)
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.user != subject.author and request.user in users:
            messages.error(request, 'Вы вошли как админ для редактирования курса.')
        section = Section.objects.get(id=section_id)
        context = {
            'subject': subject,
            'section': section,
        }
        return render(request, 'workshop/new_lecture_page.html', context)
    else:
        logout(request)
        return redirect('login')

def create_new_lecture(request, subject_id, section_id):
    if request.user.is_authenticated:
        subject=MainSubject.objects.get(id=subject_id)
        section = Section.objects.get(id=section_id)
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == 'POST':
            title = request.POST['title']
            numberOfLectures=Lecture.objects.filter(subject=subject).count()

            lecture=Lecture.objects.create(
                subject=subject,
                section=section,
                title=title,
                author=subject.author,
                
            )
            lectures=Lecture.objects.filter(subject=subject).order_by('enumerator')
            sections=Section.objects.filter(course=subject).order_by('enumerator')
            
            i=1
            for section in sections:
                for lecture in lectures:
                    if lecture.section==section:
                        lecture.enumerator=i
                        lecture.save()
                        i=i+1

            
            lectures = Lecture.objects.filter(section=section).order_by('enumerator')
            context = {
                'subject': subject,
                'section': section,
                'lectures': lectures,
            }
            return redirect('sections', subject_id )
    else:
        logout(request)
        return redirect('login')

def delete_lecture(request, lecture_id):
    if request.user.is_authenticated:
        lecture = Lecture.objects.get(id=lecture_id)
        subject = lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if subject.ready == True and subject.being_edited == False:
            messages.error(request, 'Вы не можете удалить лекцию, загруженную на сервер.')
            return redirect('sections', subject.id)
        else:
            lecture.delete()
            lectures = Lecture.objects.filter(subject=subject).order_by('enumerator')
            i=1
            for lecture in lectures:
                lecture.enumerator = i
                lecture.save()
                i=i+1
            return redirect('sections', subject.id)
    else:
        logout(request)
        return redirect('login')

def delete_lecture_videofile (request, lecture_id):
    if request.user.is_authenticated:
        lecture = Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        lecture.video_file.delete()
        lecture.save()
        return redirect ('edit_lecture', lecture.id)

    else:
        logout(request)
        return redirect('login')

def lecture_update_from_lib (request, lecture_id, v_file_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        vfile=Library.objects.get(id=v_file_id)
        lecture.video_file=vfile.video_file
        lecture.length=vfile.length
        lecture.length_1=vfile.length_1
        lecture.size_mb=vfile.size_mb
        lecture.save()
        return redirect ('sections', subject.id)
    else:
        logout(request)
        return redirect('login')

def lecture_update_videofile (request, subject_id, section_id, lecture_id):
    if request.user.is_authenticated:
        subject=MainSubject.objects.get(id=subject_id)
        section=Section.objects.get(id=section_id)
        lecture=Lecture.objects.get(id=lecture_id)
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == "POST":
            video_file = request.FILES['file']
            video_file_name = video_file.file.name
        if not video_file_name.endswith('.mp4'):
            messages.error(request, 'Некорректный форма файла. Используйте файл в формате MP4.')
            return redirect('edit_lecture', lecture.id)

        size_bytes = os.path.getsize(video_file_name)
        size_mbytes = size_bytes/1024/1024
        if size_mbytes > 950:
            messages.error(request, 'Размер файла больше 950МБ. Попробуйте использовать файлы меньшего размера.')
            return redirect('edit_lecture', lecture.id)
        #=======Module for calculating length of a lecture in two formats=======================
        clip = VideoFileClip(video_file_name)
        length=clip.duration # overall duration in seconds
        length=length // 1#getting rid of microseconds
        length_hours=length // 3600 #hours
        if length_hours < 1:
            length_hours=0
        remainder=length - length_hours * 3600
        length_min = remainder // 60 #minutes
        length_sec = remainder % 60 #seconds
        duration=datetime.timedelta(hours=length_hours, minutes=length_min, seconds=length_sec)
        #===================End of Length Module==============================
        size_mb = size_mbytes
        lecture.video_file=video_file
        lecture.length=length
        lecture.length_1=duration
        lecture.size_mb=size_mb
        lecture.save()
        #subtitle_file = request.POST.get('subtitle_file', False)
        #subtitle_file=subtitle_file,
        # translation_file=translation_file,
        return redirect ('edit_lecture', lecture.id)
    else:
        logout(request)
        return redirect('login')

def edit_lecture_title (request, lecture_id):
    if request.user.is_authenticated:
        lecture = Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == "POST":
            title=request.POST['title']
            lecture.title = title
            lecture.save()
            return redirect ('edit_lecture', lecture.id)
    else:
        logout(request)
        return redirect('login')

def edit_lecture(request, lecture_id):
    if request.user.is_authenticated:
        lecture = Lecture.objects.get(id=lecture_id)
        subject = lecture.subject
        section = lecture.section
        v_files=Library.objects.filter(subject=subject)
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if subject.ready == True and subject.being_edited == False:
            messages.error(request, 'Вы не можете редактировать лекции, загруженные на сервер.')
            return redirect('sections', subject.id)
        else:
            if request.user != subject.author and request.user in users:
                messages.error(request, 'Вы вошли как админ для редактирования курса.')
            if request.method == "POST":
                lecture_new = request.POST.get('lecture_id', False)
                title = request.POST['title']
                enumerator = request.POST['enumerator']
                additional_file = request.FILES.get('additional_file', False)
                url_link = request.POST.get('url_link', False)
                subtitle_file = request.POST.get('subtitle_file', False)
                #video_file = request.FILES['video_file']
                # translation_file = request.FILES['translation_file']
                #if video_file.name.endswith('.mp4'):
                #    lecture.video_file=video_file
                #    lecture.title = request.POST['title']
                #    lecture.enumerator = request.POST['enumerator']
                #    lecture.save()
                #    path = lecture.video_file.path
                #    size_bytes = os.path.getsize(path)
                #    size_mbytes = size_bytes / 1024 / 1024
                #    lecture.size_mbytes = size_mbytes
                #    lecture.save()
                #    if lecture.size_mb > 500:
                #        lecture.delete()
                #        messages.error(request, 'Видео файл слишком большого размера. Лекция удалена. Создайте ее еще раз с файлом меньшего размера.')
                #        return redirect('edit_section', subject.id, section.id)
                #    else: 
                

                if (lecture_id == int(lecture_new)):
                    lecture=Lecture.objects.get(id=lecture_id)
                    lecture.title=title
                    lecture.enumerator = enumerator
                    lecture.save()
                else:
                    print('no')
                    if Lecture.objects.filter(id=lecture_new, subject=subject, section=section, enumerator__isnull= True).exists():
                        lecture=Lecture.objects.get(id=lecture_id)
                        lecture.enumerator = None
                        lecture.save()
                        if AdditionalMaterialLink.objects.filter(lecture=lecture).exists():
                            item=AdditionalMaterialLink.objects.get(lecture=lecture)
                            item.delete()
                        if AdditionalMaterialFile.objects.filter(lecture=lecture).exists():
                            item=AdditionalMaterialFile.objects.get(lecture=lecture)
                            item.delete()
                        lecture=Lecture.objects.get(id=lecture_id_new)
                        lecture.title=title
                        lecture.enumerator = enumerator
                        lecture.save()
                    else:
                        lecture_ready=Lecture.objects.get(id=lecture_new)
                        string=f'Данный видеофайл уже используется в лекции {lecture_ready.enumerator}. Для того, чтобы снова использовать данный видеофайл, необходимо предварительно удалить лекцию {lecture_ready.enumerator}. '
                        messages.error(request, string)
                        return redirect('edit_section', subject.id, section.id)
                if url_link:
                    if AdditionalMaterialLink.objects.filter(lecture=lecture).exists():
                        item=AdditionalMaterialLink.objects.get(lecture=lecture)
                        item.url_link=url_link
                        item.save()
                    else:
                        AdditionalMaterialLink.objects.create(
                            lecture=lecture,
                            url_link=url_link
                        )
                else:
                    if AdditionalMaterialLink.objects.filter(lecture=lecture).exists():
                        item=AdditionalMaterialLink.objects.get(lecture=lecture)
                        item.delete()
                
                if additional_file:
                    if additional_file.name.endswith('.doc') or additional_file.name.endswith('.png') or additional_file.name.endswith('.gif') or additional_file.name.endswith('.bmp') or additional_file.name.endswith('.rar') or additional_file.name.endswith('.jpeg') or additional_file.name.endswith('.zip') or additional_file.name.endswith('.pdf') or additional_file.name.endswith('.txt') or additional_file.name.endswith('.jpg'):
                        if AdditionalMaterialFile.objects.filter(lecture=lecture).exists():
                            item=AdditionalMaterialFile.objects.get(lecture=lecture)
                            item.additional_file=additional_file
                            item.save()
                        else:
                            AdditionalMaterialFile.objects.create(
                                lecture=lecture,
                                additional_file=additional_file
                            )
                    else:
                        messages.error(request, 'Лекция отредактирована, но дополнитеьный файл не был загружен,так как вы использовали некорректный формат файла..')
                        return redirect('edit_section', subject.id, section.id)
                else:
                    if AdditionalMaterialFile.objects.filter(lecture=lecture).exists():
                        item=AdditionalMaterialFile.objects.get(lecture=lecture)
                        item.delete()
                        
                lectures = Lecture.objects.filter(subject=subject)
                context = {
                    'lectures': lectures,
                    'section': section,
                    'subject': subject
                }
                return redirect('edit_section', subject.id, section.id)
                #else:
                #   messages.error(request, 'File has inproper format. Load mp4 file')
                #    messages.error(request, 'Некорректный формат файла. Загрузите файл в формате mp4.')
                #   return redirect('edit_section', subject.id, section.id)
            else:
                context = {
                    'lecture': lecture,
                    'subject': subject,
                    'section': section,
                    'v_files': v_files,
                }
                return render(request, 'workshop/edit_lecture_page.html', context)
    else:
        logout(request)
        return redirect('login')

#==============================Multiple Files Uploading========================
def upload_multiple_files (request, subject_id):
    if request.user.is_authenticated: 
        subject=MainSubject.objects.get(id=subject_id)
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == "POST":
            author = request.user
            v_files= request.FILES.getlist ('multiple_files')
            for v_file in v_files:
                video_file_name = v_file.file.name
                if not video_file_name.endswith('.mp4'):
                    string=f'Некорректный формат файла. Файл {video_file_name} и все последующие не загружены. Используйте корректный формат файла.'
                    messages.error(request, string)
                    return redirect('edit_subject', subject_id)
                size_bytes = os.path.getsize(video_file_name)
                size_mbytes = size_bytes/1024/1024
                # if size_mbytes > 200:
                #     messages.error(request, 'Размер файла больше 200МБ. Попробуйте использовать файлы меньшего размера.')
                #     return redirect('edit_section', subject_id, section_id)

                #=======Module for calculating length of a lecture in two formats=======================
                clip = VideoFileClip(video_file_name)
                length=clip.duration # overall duration in seconds
                length=length // 1#getting rid of microseconds
                length_hours=length // 3600 #hours
                if length_hours < 1:
                    length_hours=0
                remainder=length - length_hours * 3600
                length_min = remainder // 60 #minutes
                length_sec = remainder % 60 #seconds
                duration=datetime.timedelta(hours=length_hours, minutes=length_min, seconds=length_sec)
                #===================End of Length Module==============================

                size_mb = size_mbytes
                v_file = Library.objects.create(
                    video_file=v_file,
                    #subtitle_file=subtitle_file,
                    # translation_file=translation_file,
                    author=author,
                    #section=section,
                    subject=subject,
                    #free=free_access,
                    length=length,
                    length_1=duration,
                    size_mb=size_mb,
                )
            return redirect ('edit_subject', subject.id)
    else:
        logout(request)
        return redirect('login')

def bulk_lecture_enumerator_update (request, subject_id):
    if request.user.is_authenticated:
        subject=MainSubject.objects.get(id=subject_id)
        sections=Section.objects.filter(course=subject).order_by('-enumerator')
        lectures=Lecture.objects.filter(subject=subject).order_by('-enumerator')
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == "POST":
            sec_lec_ids = request.POST.getlist("sec_lec_id", None)
            section_ids = request.POST.getlist("section_id", None)
            i_sec=0
            i=0
            for section_id in section_ids:
                section=Section.objects.get(id=section_id)
                section.enumerator=i_sec+1
                section.save()
                i_sec=i_sec+1
                for sec_lec_id in sec_lec_ids:
                    if section_id in sec_lec_id:
                        n=sec_lec_id.index('/')
                        #lecture_id=sec_lec_id.replace('section_id', '')#changin a part of the string for a new one
                        lecture_id=sec_lec_id[n+1:]# deleting the number of elements in the string
                        lecture=Lecture.objects.get(id=lecture_id)
                        lecture.section=section
                        lecture.enumerator=i+1
                        lecture.save()
                        i=i+1
            return redirect ('sections', subject.id)
        else:
            context = {
                'subject': subject,
                'sections': sections,
                'lectures': lectures,
            }
            return render(request, 'workshop/sections.html', context)
    else:
        logout(request)
        return redirect('login')

#========================================================================
def quiz_creation (request, lecture_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        answers=[]
        questions=QuizQuestion.objects.filter(lecture=lecture)
        for question in questions:
            answers=QuizAnswer.objects.filter(question=question)
        #     answers.append(answer)
        context = {
            'questions': questions,
            'answers': answers,
            'lecture': lecture,
            'subject': subject,
        }
        return render (request, 'workshop/quiz_creation_page.html', context)
    else:
        logout(request)
        return redirect('login') 

def create_quiz(request, lecture_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == "POST":
            question = request.POST["question"]
            text_answers = request.POST.getlist("text_answer", None)
            correct=request.POST['answer']
            quest=QuizQuestion.objects.create(
                    question=question,
                    lecture=lecture
                )
            for t_answer in text_answers:
                answ=QuizAnswer.objects.create(
                    lecture=lecture,
                    question=quest,
                    answer=t_answer,
                )
                if correct == answ.answer:
                    answ.correct=True
                    answ.save()
                
            return redirect ('quiz_creation', lecture.id)

    else:
        logout(request)
        return redirect('login')

def edit_quiz_question (request, lecture_id, question_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == "POST":
            question=QuizQuestion.objects.get(id=question_id)
            question.delete()
            
            question = request.POST["question"]
            text_answers = request.POST.getlist("text_answer", None)
            correct=request.POST['answer']
            quest=QuizQuestion.objects.create(
                    question=question,
                    lecture=lecture
                )
            for t_answer in text_answers:
                answ=QuizAnswer.objects.create(
                    lecture=lecture,
                    question=quest,
                    answer=t_answer,
                )
                if correct == answ.answer:
                    answ.correct=True
                    answ.save()
                    
            return redirect ('quiz_creation', lecture.id)
    else:
        logout(request)
        return redirect('login')

def delete_quiz_question (request, lecture_id, question_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        question=QuizQuestion.objects.get(id=question_id)
        question.delete()
        return redirect ('quiz_creation', lecture.id)
    else:
        logout(request)
        return redirect('login')

def delete_quiz (request, lecture_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        questions=lecture.quizquestion_set.all()
        for question in questions:
            question.delete()
        return redirect ('edit_lecture', lecture.id)
    else:
        logout(request)
        return redirect('login')

#===============================================================

def add_text_file (request, lecture_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == "POST":
            additional_file = request.FILES["file"]
            if additional_file.name.endswith('.doc') or additional_file.name.endswith('.png') or additional_file.name.endswith('.gif') or additional_file.name.endswith('.bmp') or additional_file.name.endswith('.rar') or additional_file.name.endswith('.jpeg') or additional_file.name.endswith('.zip') or additional_file.name.endswith('.pdf') or additional_file.name.endswith('.txt') or additional_file.name.endswith('.jpg'):
                textFile=AdditionalMaterialFile.objects.create(
                    lecture=lecture,
                    additional_file=additional_file
                )
            else:
                messages.error(request, 'Некорректный формат текстового файла.')
            return redirect ('edit_lecture', lecture.id)
    else:
        logout(request)
        return redirect('login')

def delete_text_file (request, lecture_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        files=lecture.additionalmaterialfile_set.all()
        for file in files:
            file.delete()
        return redirect ('edit_lecture', lecture.id)
    else:
        logout(request)
        return redirect('login')

#====================================================

def add_url_link (request, lecture_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        if request.method == "POST":
            url_link = request.POST["url_link"]
            url_link=AdditionalMaterialLink.objects.create(
                    lecture=lecture,
                    url_link=url_link,
                )
        return redirect ('edit_lecture', lecture.id)
    else:
        logout(request)
        return redirect('login')

def delete_url_link (request, lecture_id):
    if request.user.is_authenticated:
        lecture=Lecture.objects.get(id=lecture_id)
        subject=lecture.subject
        users=Group.objects.get(name='admin').user_set.all()
        if request.user != subject.author and request.user not in users:
            logout(request)
            return redirect('login')
        links=lecture.additionalmateriallink_set.all()
        for link in links:
            link.delete()
        return redirect ('edit_lecture', lecture.id)
    else:
        logout(request)
        return redirect('login')

#===============================================================
def video(request, subject_id, lecture_id):
    # if not request.user.is_authenticated:
    #     return redirect('login')

    subject = get_object_or_404(MainSubject, id=subject_id)
    the_video = get_object_or_404(Lecture, id=lecture_id)

    # if not (Transaction.objects.filter(buyer=request.user, course=subject).exists()
    #         or request.user == subject.author
    #         or the_video.free == True):
    #     messages.error(request, 'Для просмотра видео вам необходимо приобрести данный курс.')
    #     return redirect('login')

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
        users=Group.objects.get(name='admin').user_set.all()
        if subject.ready == False:
            if request.user != subject.author:
                logout(request)
                return redirect('login')
            if Lecture.objects.filter(subject=subject.id).exists():
                badwords=Badword.objects.all()
                lectures = Lecture.objects.filter(subject=subject).order_by('enumerator')
                # lectures = Lecture.objects.filter(subject=subject, enumerator__isnull=False).order_by.('enumerator')
                subject_duration=0
                for lecture in lectures:
                    subject_duration += lecture.length #in seconds
                
                #========Length Module for Subject================================
                length_hours=subject_duration // 3600 #hours
                if length_hours < 1:
                    length_hours=0
                remainder=subject_duration-length_hours*3600
                length_min = remainder // 60 #minutes
                length_sec = remainder % 60 #seconds
                duration=datetime.timedelta(hours=length_hours, minutes=length_min, seconds=length_sec)
                subject.length = subject_duration
                subject.length_1=duration
                subject.save()
                #==============End of Length Module for Subject
                #=================Length Module for section==========================
                sections = Section.objects.filter(course=subject)
                for section in sections:
                    lectures_length=lectures.filter(section=section)
                    section_length=0
                    for lecture_length in lectures_length:
                        section_length += lecture_length.length

                    length_hours=section_length // 3600 #hours
                    if length_hours < 1:
                        length_hours=0
                    remainder=section_length-length_hours*3600
                    length_min = remainder // 60 #minutes
                    length_sec = remainder % 60 #seconds
                    duration=datetime.timedelta(hours=length_hours, minutes=length_min, seconds=length_sec)
                section.length=section_length
                section.length_1=duration
                section.save()
                #=====================End of Length Module for Section=======================
                #============Check for Badwords Module=================================
                if badwords:
                    for word in badwords:
                        if word.badword in subject.title:
                            subject.blocked = True
                            subject.save()
                            messages.error(request, 'Курс не был загружен. Измените название курса.')
                            return redirect('edit_subject', subject.id)     
                        for section in sections:
                            if word.badword in section.title:
                                section.blocked = True
                                section.save()
                                subject.blocked = True
                                subject.save()
                                messages.error(request, 'Курс не был загружен. Измените название одного из разделов.')
                                return redirect('edit_subject', subject.id)
                        for lecture in lectures:
                            if word.badword in lecture.title:
                                lecture.blocked = True
                                lecture.save()
                                subject.blocked = True
                                subject.save()
                                messages.error(request, 'Курс не был загружен. Измените название одной из лекций.')
                                return redirect('edit_subject', subject.id)
                subject.checked = True
                subject.ready=True
                subject.save()
                #================End of Check for Badwords Module===========================
                #===============sending lectures to CDN=========================
                for lecture in lectures:
                    #lecture.ready = True
                    if lecture.video_file:
                        lecture.ready = True
                        lecture.processing_state = PROCESSING_READY_TO_START
                    lecture.save()
                #==========================================================
                return redirect('studio')      
            else:
                subject_id=subject.id
                messages.error(request, 'В курсе отсутствуют лекции. Пожалуйста, создайте лекции.')
                return redirect('edit_subject', subject_id)
        #=========Editing previously loaded subject===========================
        else:
            users=Group.objects.get(name='admin').user_set.all()
            if request.user != subject.author and request.user not in users:
                logout(request)
                return redirect('login')
            if Lecture.objects.filter(subject=subject.id).exists():
                lectures=Lecture.objects.filter(subject=subject.id)
                for lecture in lectures:
                    #process a new lecture which has been added
                    if lecture.ready == False:
                        #lecture.ready=True
                        if lecture.video_file:
                            lecture.ready=True
                            lecture.processing_state = PROCESSING_READY_TO_START
                        lecture.save()
            return redirect('studio')
    else:
        logout(request)
        return redirect('login')

def send_lecture (request, lecture_id):
    lecture=Lecture.objects.get(id=lecture_id)
    subject=lecture.subject
    users=Group.objects.get(name='admin').user_set.all()
    if request.user in users:   
        subject=lecture.subject
        lectures=Lecture.objects.filter(subject=subject).order_by('enumerator')
        lecture.processing_state = PROCESSING_READY_TO_START
        lecture.save()
        return redirect ('sections', subject.id)
    else:
        logout(request)
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
        if Author.objects.filter(user=request.user).exists():
            author=Author.objects.get(user=request.user)
            if Transaction.objects.filter(author=author, money_paid=True).exists():
                query = Transaction.objects.filter(author=author, money_paid=True).order_by('-date_paid')
                if 'sort_criteria' in request.GET:
                    sort_criteria = request.GET['sort_criteria']
                    if sort_criteria == 'sell_date':
                        query = query.order_by('-date_paid')
                    elif sort_criteria == 'transfer_date':
                        query = query.order_by('-date_transfer')
                    elif sort_criteria == 'course_titel':
                        query = query.order_by('-course')

                paginator = Paginator(query, 50)
                page = request.GET.get('page')
                query_paged = paginator.get_page(page)

                context = {
                    'query': query_paged
                }
                return render(request, 'workshop/transactions.html', context)
            else:
                messages.error(request, 'Вы не продали ни одного курса')
                return render(request, 'workshop/transactions.html')
        else:
            messages.error(request, 'Вы не загрузили ни одного курса')
            return render(request, 'workshop/transactions.html')
           
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

