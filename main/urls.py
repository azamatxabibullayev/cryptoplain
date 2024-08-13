from django.urls import path
from . import views

urlpatterns = [
    path('video-lessons/', views.video_lessons_view, name='video_lessons'),
    path('informations/', views.information, name='information'),
    path('information/<int:info_id>/', views.information_detail, name='information_detail'),
]
