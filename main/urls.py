from django.urls import path
from . import views

urlpatterns = [
    path('video-lessons/', views.video_lessons_view, name='video_lessons'),
    path('informations/', views.information, name='information'),
    path('birja/', views.birja_view, name='birja'),
    path('information/<int:info_id>/', views.information_detail, name='information_detail'),
    path('advice/', views.advices_view, name='advice'),
    path('signal/', views.signals_view, name='signal'),
    path('news/', views.news_view, name='news'),
    path('analyses/', views.analysis_view, name='analyses'),
    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('notes/<int:pk>/', views.note_details, name='note_details'),
    path('lessons/', views.lesson_view, name='lessons'),
    path('lessons/<int:id>/', views.lesson_detail, name='lesson_detail'),
    path('indicators/', views.indicator_view, name='indicators'),
    path('indicators/<int:id>/', views.indicator_detail, name='indicator_detail'),
    path('books/', views.books_view, name='books'),
    path('books/<int:book_id>/', views.book_view, name='book_view'),
    path('mobile/', views.mobile_landing, name='mobile'),
    path('mobile/lessons', views.mobile_lessons, name='mobile_lessons'),
]
