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
]
