from collections import defaultdict
from home.models import FearGreedIndex
from .forms import NoteForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localdate
from .models import VideoLesson, Information, Birja, Advice, Signal, News, Analysis, Lesson, Note, Indicator, Book
from django.db.models import Q
from django.core.paginator import Paginator


def video_lessons_view(request):
    query = request.GET.get('q')
    if query:
        video_lessons = VideoLesson.objects.filter(
            Q(title__icontains=query)
        )
    else:
        video_lessons = VideoLesson.objects.order_by('-id')
    paginator = Paginator(video_lessons, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'main/video_lessons.html', context)


def information(request):
    query = request.GET.get('q')
    if query:
        information_list = Information.objects.filter(
            Q(title__icontains=query) | Q(info_text__icontains=query)
        )
    else:
        information_list = Information.objects.order_by('-id')

    paginator = Paginator(information_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'information_list': page_obj,
        'page_obj': page_obj
    }
    return render(request, 'main/informations.html', context)


def information_detail(request, info_id):
    information = get_object_or_404(Information, id=info_id)
    page_number = request.GET.get('page', 1)
    context = {
        'information': information,
        'page_number': page_number,
    }
    return render(request, 'main/information_detail.html', context)


def birja_view(request):
    birja = Birja.objects.order_by('-id')

    paginator = Paginator(birja, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'birja': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'main/birja.html', context)


def advices_view(request):
    advice = Advice.objects.order_by('-id')

    paginator = Paginator(advice, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'advice': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'main/advice.html', context)


def signals_view(request):
    signal = Signal.objects.order_by('-id')
    context = {
        'signal': signal
    }
    return render(request, 'main/signal.html', context)


def news_view(request):
    news = News.objects.order_by('-id')
    context = {
        'news': news
    }
    return render(request, 'main/news.html', context)


def analysis_view(request):
    user = request.user
    accessible_analyses = Analysis.objects.none()
    inaccessible_analyses = Analysis.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            user_type = user.premium_user.premium_type
            if user_type == 'pro':
                accessible_analyses = Analysis.objects.filter(analysis_type__in=['normal', 'standard', 'pro'])
            elif user_type == 'standard':
                accessible_analyses = Analysis.objects.filter(analysis_type__in=['normal', 'standard'])
                inaccessible_analyses = Analysis.objects.filter(analysis_type='pro')
            else:
                accessible_analyses = Analysis.objects.filter(analysis_type='normal')
                inaccessible_analyses = Analysis.objects.filter(analysis_type__in=['standard', 'pro'])
        else:
            accessible_analyses = Analysis.objects.filter(analysis_type='normal')
            inaccessible_analyses = Analysis.objects.filter(analysis_type__in=['standard', 'pro'])

    grouped_accessible_analyses = defaultdict(list)
    grouped_inaccessible_analyses = defaultdict(list)


    for analysis in accessible_analyses:
        date = localdate(analysis.created_at)
        grouped_accessible_analyses[date].append(analysis)

    for analysis in inaccessible_analyses:
        date = localdate(analysis.created_at)
        grouped_inaccessible_analyses[date].append(analysis)


    combined_analyses = {}
    all_dates = sorted(
        set(grouped_accessible_analyses.keys()).union(set(grouped_inaccessible_analyses.keys())),
        reverse=True
    )
    for date in all_dates:
        combined_analyses[date] = {
            'accessible': grouped_accessible_analyses.get(date, []),
            'inaccessible': grouped_inaccessible_analyses.get(date, [])
        }

    context = {
        'combined_analyses': combined_analyses,
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
            return redirect('note_details', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'main/note_edit.html', {'form': form, 'note': note})


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
                lessons = Lesson.objects.order_by('-id').filter(lesson_type__in=['normal', 'standard', 'pro'])
            else:
                lessons = Lesson.objects.order_by('-id').filter(lesson_type__in=['normal', 'standard'])
        else:
            lessons = Lesson.objects.order_by('-id').filter(lesson_type='normal')
    else:
        lessons = Lesson.objects.order_by('-id').filter(lesson_type='normal')

    paginator = Paginator(lessons, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'lessons': page_obj,
        'page_obj': page_obj,
        'is_premium': hasattr(user, 'premium_user'),
    }
    return render(request, 'main/lessons.html', context)


def lesson_detail(request, id):
    lesson = Lesson.objects.get(id=id)
    page_number = request.GET.get('page', 1)
    context = {
        'lesson': lesson,
        'page_number': page_number,
    }
    return render(request, 'main/lesson_detail.html', context)


def indicator_view(request):
    query = request.GET.get('q', None)
    user = request.user
    indicators = Indicator.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            if user.premium_user.premium_type == 'pro':
                indicators = Indicator.objects.order_by('-id').filter(
                    Q(indicator_type__in=['normal', 'standard', 'pro'])
                )
            else:
                indicators = Indicator.objects.order_by('-id').filter(
                    Q(indicator_type__in=['normal', 'standard'])
                )
        else:
            indicators = Indicator.objects.order_by('-id').filter(
                Q(indicator_type='normal')
            )
    else:
        indicators = Indicator.objects.order_by('-id').filter(
            Q(indicator_type='normal')
        )

    if query:
        indicators = indicators.filter(
            Q(title__icontains=query) | Q(indicator_text__icontains=query)
        )

    paginator = Paginator(indicators, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'indicators': page_obj,
        'page_obj': page_obj,
        'user_type': getattr(user, 'user_type', 'anonymous'),
        'is_premium': hasattr(user, 'premium_user'),
        'query': query,
    }
    return render(request, 'main/indicators.html', context)


def indicator_detail(request, id):
    indicator = Indicator.objects.get(id=id)
    page_number = request.GET.get('page', 1)

    context = {
        'indicator': indicator,
        'page_number': page_number,
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


# MOBILE MODE

def mobile_landing(request):
    fear_greed_index_image = FearGreedIndex.objects.last()
    context = {
        'fear_greed_index_image': fear_greed_index_image,
    }
    return render(request, 'landing_page_mobile.html', context)


def mobile_lessons(request):
    user = request.user
    lessons = Lesson.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            user_type = user.premium_user.premium_type
            if user_type == 'pro':
                lessons = Lesson.objects.order_by('-id').filter(lesson_type__in=['normal', 'standard', 'pro'])
            else:
                lessons = Lesson.objects.order_by('-id').filter(lesson_type__in=['normal', 'standard'])
        else:
            lessons = Lesson.objects.order_by('-id').filter(lesson_type='normal')
    else:
        lessons = Lesson.objects.order_by('-id').filter(lesson_type='normal')

    paginator = Paginator(lessons, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'lessons': page_obj,
        'page_obj': page_obj,
        'is_premium': hasattr(user, 'premium_user'),
    }
    return render(request, 'main/lessons_mobile.html', context)


def mobile_lesson_detail(request, id):
    lesson = Lesson.objects.get(id=id)
    page_number = request.GET.get('page', 1)

    context = {
        'lesson': lesson,
        'page_number': page_number,
    }
    return render(request, 'main/lesson_detail_mobile.html', context)


def mobile_video_lessons_view(request):
    query = request.GET.get('q')
    if query:
        video_lessons = VideoLesson.objects.filter(
            Q(title__icontains=query)
        )
    else:
        video_lessons = VideoLesson.objects.order_by('-id')

    paginator = Paginator(video_lessons, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'video_lessons': page_obj,
        'page_obj': page_obj
    }
    return render(request, 'main/video_lessons_mobile.html', context)


def mobile_advices_view(request):
    advice = Advice.objects.order_by('-id')
    paginator = Paginator(advice, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'advice': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'main/advice_mobile.html', context)


def mobile_birja_view(request):
    birja = Birja.objects.order_by('-id')

    paginator = Paginator(birja, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'birja': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'main/birja_mobile.html', context)


def mobile_information(request):
    query = request.GET.get('q')
    if query:
        information_list = Information.objects.filter(
            Q(title__icontains=query) | Q(info_text__icontains=query)
        )
    else:
        information_list = Information.objects.order_by('-id')

    paginator = Paginator(information_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'information_list': page_obj,
        'page_obj': page_obj
    }
    return render(request, 'main/informations_mobile.html', context)


def mobile_information_detail(request, info_id):
    information = get_object_or_404(Information, id=info_id)
    page_number = request.GET.get('page', 1)
    context = {
        'information': information,
        'page_number': page_number,
    }
    return render(request, 'main/information_detail_mobile.html', context)


def mobile_signals_view(request):
    signal = Signal.objects.order_by('-id')
    context = {
        'signal': signal
    }
    return render(request, 'main/signal_mobile.html', context)


def mobile_books_view(request):
    return render(request, 'main/books_mobile.html')


def mobile_news_view(request):
    news = News.objects.order_by('-id')
    context = {
        'news': news
    }
    return render(request, 'main/news_mobile.html', context)


def mobile_indicator_view(request):
    query = request.GET.get('q', None)
    user = request.user
    indicators = Indicator.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            if user.premium_user.premium_type == 'pro':
                indicators = Indicator.objects.order_by('-id').filter(
                    Q(indicator_type__in=['normal', 'standard', 'pro'])
                )
            else:
                indicators = Indicator.objects.order_by('-id').filter(
                    Q(indicator_type__in=['normal', 'standard'])
                )
        else:
            indicators = Indicator.objects.order_by('-id').filter(
                Q(indicator_type='normal')
            )
    else:
        indicators = Indicator.objects.order_by('-id').filter(
            Q(indicator_type='normal')
        )

    if query:
        indicators = indicators.filter(
            Q(title__icontains=query) | Q(indicator_text__icontains=query)
        )

    paginator = Paginator(indicators, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'indicators': page_obj,
        'page_obj': page_obj,
        'user_type': getattr(user, 'user_type', 'anonymous'),
        'is_premium': hasattr(user, 'premium_user'),
        'query': query,
    }
    return render(request, 'main/indicators_mobile.html', context)


def mobile_indicator_detail(request, id):
    indicator = Indicator.objects.get(id=id)
    page_number = request.GET.get('page', 1)

    context = {
        'indicator': indicator,
        'id': indicator.id,
        'page_number': page_number,

    }
    return render(request, 'main/indicator_detail_mobile.html', context)


def mobile_note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/note_list_mobile.html', {'notes': notes})


def mobile_note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('mobile_note_list')
    else:
        form = NoteForm()
    return render(request, 'main/note_form_mobile.html', {'form': form})


def mobile_note_details(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'main/note_details_mobile.html', {'note': note, 'id': pk})


def mobile_note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('mobile_note_details', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'main/note_edit_mobile.html', {'form': form, 'note': note})


def mobile_note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('mobile_note_list')
    return render(request, 'main/note_confirm_delete_mobile.html', {'note': note})


def mobile_analysis_view(request):
    user = request.user
    accessible_analyses = Analysis.objects.none()
    inaccessible_analyses = Analysis.objects.none()

    # Check user subscription type
    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            user_type = user.premium_user.premium_type
            if user_type == 'pro':
                accessible_analyses = Analysis.objects.filter(analysis_type__in=['normal', 'standard', 'pro'])
            elif user_type == 'standard':
                accessible_analyses = Analysis.objects.filter(analysis_type__in=['normal', 'standard'])
                inaccessible_analyses = Analysis.objects.filter(analysis_type='pro')
            else:
                accessible_analyses = Analysis.objects.filter(analysis_type='normal')
                inaccessible_analyses = Analysis.objects.filter(analysis_type__in=['standard', 'pro'])
        else:
            accessible_analyses = Analysis.objects.filter(analysis_type='normal')
            inaccessible_analyses = Analysis.objects.filter(analysis_type__in=['standard', 'pro'])

    grouped_accessible_analyses = defaultdict(list)
    grouped_inaccessible_analyses = defaultdict(list)


    for analysis in accessible_analyses:
        date = localdate(analysis.created_at)
        grouped_accessible_analyses[date].append(analysis)

    for analysis in inaccessible_analyses:
        date = localdate(analysis.created_at)
        grouped_inaccessible_analyses[date].append(analysis)


    combined_analyses = {}
    all_dates = sorted(
        set(grouped_accessible_analyses.keys()).union(set(grouped_inaccessible_analyses.keys())),
        reverse=True
    )

    for date in all_dates:
        combined_analyses[date] = {
            'accessible': grouped_accessible_analyses.get(date, []),
            'inaccessible': grouped_inaccessible_analyses.get(date, [])
        }

    context = {
        'combined_analyses': combined_analyses,
    }

    return render(request, 'main/analyses_mobile.html', context)
