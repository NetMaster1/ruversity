from django.shortcuts import render, redirect
from app_content.models import MainSubject, Lecture, Price, Category, Language, Transaction
from django.http import HttpResponseRedirect

# Create your views here.


def studio(request):
    if request.user.is_authenticated:
        my_subjects = MainSubject.objects.filter(author=request.user.id)
        context = {
            'my_subjects': my_subjects
        }
        return render(request, 'workshop/studio.html', context)
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
            thumbnail_file = request.FILES['thumbnail_file']
            lang_fkey = Language.objects.get(id=language_id)
            categ_fkey=Category.objects.get(id=category_id)
            author = request.user
            price = Price.objects.get(id=1)

            new_subject = MainSubject.objects.create(
                title=title,
                thumbnail_file=thumbnail_file,
                author=author,
                price=price,
                category=categ_fkey,
                language=lang_fkey
            )
            my_subjects = MainSubject.objects.filter(author=request.user)
            context = {
                'my_subjects': my_subjects
            }
            return render(request, 'workshop/studio.html', context)
        else:
            return render(request, 'workshop/create_new_subject.html', context)
    else:
        return redirect('login')


def edit_subject(request, subject_id):
    if request.user.is_authenticated:
        # if request.method == 'POST':
        subject = MainSubject.objects.get(id=subject_id)
        lectures = Lecture.objects.filter(course=subject)
        context = {
            'subject': subject,
            'lectures': lectures
        }
        return render(request, 'workshop/edit_subject.html', context)
    else:
        return redirect('login')


def create_new_lecture(request, subject_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            subject = MainSubject.objects.get(id=subject_id)
            title = request.POST['title']
            video_file = request.FILES['video_file']
            author = request.user
            lecture = Lecture.objects.create(
                title=title,
                video_file=video_file,
                author=author,
                course=subject,
            )
            lectures = Lecture.objects.filter(course=subject)
            context = {
                'subject': subject,
                'lectures': lectures
            }
            return render(request, 'workshop/edit_subject.html', context)
        else:
            # subject = MainSubject.objects.get(id=subject_id)
            # lectures = Lecture.objects.filter(course=subject)
            # context = {
            #     'subject': subject,
            #     'lectures': lectures
            # }
            # return render(request, 'workshop/edit_subject.html', context)
            return redirect('edit_subject')

    else:
        return redirect('login')


def edit_lecture(request, lecture_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            lecture = Lecture.objects.get(id=lecture_id)

            title = request.POST['title']
            lecture.video_file = request.FILES['video_file']
            lecture.title = request.POST['title']
            lecture.save()
            subject = lecture.course
            lectures = Lecture.objects.filter(course=subject)

            context = {
                'lectures': lectures,
                'subject': subject
            }
            return render(request, 'workshop/edit_subject.html', context)
        else:
            return redirect('edit_subject')
    else:
        return redirect('login')


def delete_lecture(request, lecture_id):
    if request.user.is_authenticated:
        lecture = Lecture.objects.get(id=lecture_id)
        subject = lecture.course
        lecture.delete()
        lectures = Lecture.objects.filter(course=subject)
        context = {
            'lectures': lectures,
            'subject': subject
        }
        return render(request, 'workshop/edit_subject.html', context)
    else:
        return redirect('login')


def video(request, lecture_id):
    if request.user.is_authenticated:
        the_video = Lecture.objects.get(id=lecture_id)
        comments = Review.objects.filter(video=video_id)
        context = {
            'the_video': the_video,
            'comments': comments
        }
        return render(request, 'video.html', context)
    else:
        return render('login')
