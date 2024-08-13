from django.contrib import admin
from .models import VideoLesson, Information, Birja, Advice, Signal, News


@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_link')


admin.site.register(Information)
admin.site.register(Birja)
admin.site.register(Advice)
admin.site.register(Signal)
admin.site.register(News)
