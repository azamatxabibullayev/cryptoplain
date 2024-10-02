from modeltranslation.translator import register, TranslationOptions
from .models import VideoLesson, Information, Birja, Advice, Signal, News, Analysis, Note, Lesson, Indicator, Book


@register(VideoLesson)
class VideolessonTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Information)
class InformationTranslationOptions(TranslationOptions):
    fields = ('title', 'info_text')


@register(Birja)
class BirjaTranslationOptions(TranslationOptions):
    fields = ('birja_name',)


@register(Advice)
class AdviceTranslationOptions(TranslationOptions):
    fields = ('advice_title', 'advice_text')


@register(Signal)
class SignalTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'news_text')


@register(Analysis)
class AnalysisTranslationOptions(TranslationOptions):
    fields = ('title', 'analysis_text')


@register(Note)
class NoteTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'lesson_text')


@register(Indicator)
class IndicatorTranslationOptions(TranslationOptions):
    fields = ('title', 'indicator_text')


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('name',)
