from django.shortcuts import render, get_object_or_404
from .models import VideoLesson, Information


def video_lessons_view(request):
    video_lessons = VideoLesson.objects.all()
    context = {
        'video_lessons': video_lessons
    }
    return render(request, 'main/video_lessons.html', context)


def information(request):
    information_list = Information.objects.all()
    context = {
        'information_list': information_list
    }
    return render(request, 'main/informations.html', context)


def information_detail(request, info_id):
    information = get_object_or_404(Information, id=info_id)
    context = {
        'information': information
    }
    return render(request, 'main/information_detail.html', context)
