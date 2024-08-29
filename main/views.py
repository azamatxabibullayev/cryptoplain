from collections import defaultdict
from .forms import NoteForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localdate
from .models import VideoLesson, Information, Birja, Advice, Signal, News, Analysis, Lesson, Note, Indicator, Book


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


def birja_view(request):
    birja = Birja.objects.all()
    context = {
        'birja': birja
    }
    return render(request, 'main/birja.html', context)


def advices_view(request):
    advice = Advice.objects.all()
    context = {
        'advice': advice
    }
    return render(request, 'main/advice.html', context)


def signals_view(request):
    signal = Signal.objects.all()
    context = {
        'signal': signal
    }
    return render(request, 'main/signal.html', context)


def news_view(request):
    news = News.objects.all()
    context = {
        'news': news
    }
    return render(request, 'main/news.html', context)


def analysis_view(request):
    user = request.user
    analyses = Analysis.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            user_type = user.premium_user.premium_type
            if user_type == 'pro':
                analyses = Analysis.objects.filter(analysis_type__in=['normal', 'standard', 'pro'])
            else:
                analyses = Analysis.objects.filter(analysis_type__in=['normal', 'standard'])
        else:
            analyses = Analysis.objects.filter(analysis_type='normal')
    else:
        analyses = Analysis.objects.filter(analysis_type='normal')

    grouped_analyses = defaultdict(list)
    for analysis in analyses:
        date = localdate(analysis.created_at)
        grouped_analyses[date].append(analysis)

    context = {
        'analyses': dict(grouped_analyses),
    }
    return render(request, 'main/analyses.html', context)


def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/note_list.html', {'notes': notes})


def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'main/note_form.html', {'form': form})


def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'main/note_form.html', {'form': form})


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'main/note_confirm_delete.html', {'note': note})


def note_details(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'main/note_details.html', {'note': note})


def lesson_view(request):
    user = request.user
    lessons = Lesson.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            user_type = user.premium_user.premium_type
            if user_type == 'pro':
                lessons = Lesson.objects.filter(lesson_type__in=['normal', 'standard', 'pro'])
            else:
                lessons = Lesson.objects.filter(lesson_type__in=['normal', 'standard'])
        else:
            lessons = Lesson.objects.filter(lesson_type='normal')
    else:
        lessons = Lesson.objects.filter(lesson_type='normal')

    context = {
        'lessons': lessons,
    }
    return render(request, 'main/lessons.html', context)


def lesson_detail(request, id):
    lesson = Lesson.objects.get(id=id)
    context = {
        'lesson': lesson,
    }
    return render(request, 'main/lesson_detail.html', context)


def indicator_view(request):
    user = request.user
    indicators = Indicator.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            user_type = user.premium_user.premium_type
            if user_type == 'pro':
                indicators = Indicator.objects.filter(indicator_type__in=['normal', 'standard', 'pro'])
            else:
                indicators = Indicator.objects.filter(indicator_type__in=['normal', 'standard'])
        else:
            indicators = Indicator.objects.filter(indicator_type='normal')
    else:
        indicators = Indicator.objects.filter(indicator_type='normal')

    context = {
        'indicators': indicators,
    }
    return render(request, 'main/indicators.html', context)


def indicator_detail(request, id):
    indicator = Indicator.objects.get(id=id)
    context = {
        'indicator': indicator,
    }
    return render(request, 'main/indicator_detail.html', context)


def books_view(request):
    user = request.user
    books = Book.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            user_type = user.premium_user.premium_type
            if user_type == 'pro':
                books = Book.objects.filter(book_type__in=['normal', 'standard', 'pro'])
            else:
                books = Book.objects.filter(book_type__in=['normal', 'standard'])
        else:
            books = Book.objects.filter(book_type='normal')
    else:
        books = Book.objects.filter(book_type='normal')

    context = {
        'books': books,
    }
    return render(request, 'main/books.html', context)


def book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'main/book_view.html', context)
