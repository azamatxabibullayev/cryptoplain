from collections import defaultdict
from home.models import FearGreedIndex
from .forms import NoteForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localdate
from .models import VideoLesson, Information, Birja, Advice, Signal, News, Analysis, Lesson, Note, Indicator, Book
from django.db.models import Q


def video_lessons_view(request):
    query = request.GET.get('q')
    if query:
        video_lessons = VideoLesson.objects.filter(
            Q(title__icontains=query)
        )
    else:
        video_lessons = VideoLesson.objects.all()

    context = {
        'video_lessons': video_lessons
    }
    return render(request, 'main/video_lessons.html', context)


def information(request):
    query = request.GET.get('q')
    if query:
        information_list = Information.objects.filter(
            Q(title__icontains=query) | Q(info_text__icontains=query)
        )
    else:
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

    # Group analyses by date
    for analysis in accessible_analyses:
        date = localdate(analysis.created_at)
        grouped_accessible_analyses[date].append(analysis)

    for analysis in inaccessible_analyses:
        date = localdate(analysis.created_at)
        grouped_inaccessible_analyses[date].append(analysis)

    # Combine accessible and inaccessible analyses by date
    combined_analyses = {}
    all_dates = set(grouped_accessible_analyses.keys()).union(set(grouped_inaccessible_analyses.keys()))
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
    query = request.GET.get('q')
    user = request.user
    indicators = Indicator.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            user_type = user.premium_user.premium_type
            if user_type == 'pro':
                indicators = Indicator.objects.filter(
                    Q(indicator_type__in=['normal', 'standard', 'pro']) &
                    (Q(title__icontains=query) | Q(indicator_text__icontains=query)) if query else
                    Q(indicator_type__in=['normal', 'standard', 'pro'])
                )
            else:
                indicators = Indicator.objects.filter(
                    Q(indicator_type__in=['normal', 'standard']) &
                    (Q(title__icontains=query) | Q(indicator_text__icontains=query)) if query else
                    Q(indicator_type__in=['normal', 'standard'])
                )
        else:
            indicators = Indicator.objects.filter(
                Q(indicator_type='normal') &
                (Q(title__icontains=query) | Q(indicator_text__icontains=query)) if query else
                Q(indicator_type='normal')
            )
    else:
        indicators = Indicator.objects.filter(
            Q(indicator_type='normal') &
            (Q(title__icontains=query) | Q(indicator_text__icontains=query)) if query else
            Q(indicator_type='normal')
        )

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
    return render(request, 'main/lessons_mobile.html', context)


def mobile_lesson_detail(request, id):
    lesson = Lesson.objects.get(id=id)
    context = {
        'lesson': lesson,
    }
    return render(request, 'main/lesson_detail_mobile.html', context)


def mobile_video_lessons_view(request):
    query = request.GET.get('q')
    if query:
        video_lessons = VideoLesson.objects.filter(
            Q(title__icontains=query)
        )
    else:
        video_lessons = VideoLesson.objects.all()

    context = {
        'video_lessons': video_lessons
    }
    return render(request, 'main/video_lessons_mobile.html', context)


def mobile_advices_view(request):
    advice = Advice.objects.all()
    context = {
        'advice': advice
    }
    return render(request, 'main/advice_mobile.html', context)


def mobile_birja_view(request):
    birja = Birja.objects.all()
    context = {
        'birja': birja
    }
    return render(request, 'main/birja_mobile.html', context)


def mobile_information(request):
    query = request.GET.get('q')
    if query:
        information_list = Information.objects.filter(
            Q(title__icontains=query) | Q(info_text__icontains=query)
        )
    else:
        information_list = Information.objects.all()

    context = {
        'information_list': information_list
    }
    return render(request, 'main/informations_mobile.html', context)


def mobile_information_detail(request, info_id):
    information = get_object_or_404(Information, id=info_id)
    context = {
        'information': information
    }
    return render(request, 'main/information_detail_mobile.html', context)


def mobile_signals_view(request):
    signal = Signal.objects.all()
    context = {
        'signal': signal
    }
    return render(request, 'main/signal_mobile.html', context)


def mobile_books_view(request):
    return render(request, 'main/books_mobile.html')


def mobile_news_view(request):
    news = News.objects.all()
    context = {
        'news': news
    }
    return render(request, 'main/news_mobile.html', context)


def mobile_indicator_view(request):
    query = request.GET.get('q')
    user = request.user
    indicators = Indicator.objects.none()

    if user.is_authenticated:
        if hasattr(user, 'premium_user'):
            user_type = user.premium_user.premium_type
            if user_type == 'pro':
                indicators = Indicator.objects.filter(
                    Q(indicator_type__in=['normal', 'standard', 'pro']) &
                    (Q(title__icontains=query) | Q(indicator_text__icontains=query)) if query else
                    Q(indicator_type__in=['normal', 'standard', 'pro'])
                )
            else:
                indicators = Indicator.objects.filter(
                    Q(indicator_type__in=['normal', 'standard']) &
                    (Q(title__icontains=query) | Q(indicator_text__icontains=query)) if query else
                    Q(indicator_type__in=['normal', 'standard'])
                )
        else:
            indicators = Indicator.objects.filter(
                Q(indicator_type='normal') &
                (Q(title__icontains=query) | Q(indicator_text__icontains=query)) if query else
                Q(indicator_type='normal')
            )
    else:
        indicators = Indicator.objects.filter(
            Q(indicator_type='normal') &
            (Q(title__icontains=query) | Q(indicator_text__icontains=query)) if query else
            Q(indicator_type='normal')
        )

    context = {
        'indicators': indicators,
    }
    return render(request, 'main/indicators_mobile.html', context)


def mobile_indicator_detail(request, id):
    indicator = Indicator.objects.get(id=id)
    context = {
        'indicator': indicator,
        'id': indicator.id,
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
            return redirect('mobile_note_details')
    else:
        form = NoteForm(instance=note)
    return render(request, 'main/note_form_mobile.html', {'form': form})


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

    # Group analyses by date
    for analysis in accessible_analyses:
        date = localdate(analysis.created_at)
        grouped_accessible_analyses[date].append(analysis)

    for analysis in inaccessible_analyses:
        date = localdate(analysis.created_at)
        grouped_inaccessible_analyses[date].append(analysis)

    # Combine accessible and inaccessible analyses by date
    combined_analyses = {}
    all_dates = set(grouped_accessible_analyses.keys()).union(set(grouped_inaccessible_analyses.keys()))
    for date in all_dates:
        combined_analyses[date] = {
            'accessible': grouped_accessible_analyses.get(date, []),
            'inaccessible': grouped_inaccessible_analyses.get(date, [])
        }

    context = {
        'combined_analyses': combined_analyses,
    }

    return render(request, 'main/analyses_mobile.html', context)
