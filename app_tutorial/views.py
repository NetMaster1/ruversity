from django.shortcuts import render
from .models import Tutorial

# Create your views here.


def tutorial (request):
    videos=Tutorial.objects.all()
    context = {
        "videos": videos
    }
    return render (request, 'tutorial/tutorial_list.html', context)

def video (request, video_id):
    video=Tutorial.objects.get(id=video_id)
    context = {
        'video': video,
        }
    return render(request, 'tutorial/tutorial_video.html', context)