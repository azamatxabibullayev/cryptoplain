from django.contrib import admin
from .models import VideoLesson, Information


@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_link')


admin.site.register(Information)
