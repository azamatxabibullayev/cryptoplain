from django.contrib import admin
from .models import VideoLesson, Information, Birja, Advice, Signal, News, Analysis, Note, Lesson, Indicator, Book


@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_link')


admin.site.register(Information)
admin.site.register(Birja)
admin.site.register(Advice)
admin.site.register(Signal)
admin.site.register(News)
admin.site.register(Lesson)
admin.site.register(Indicator)
admin.site.register(Book)


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('title', 'analysis_type', 'created_at')
    list_filter = ('analysis_type', 'created_at')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
