from django.urls import path
from .views import register, warning, profile_view, user_login, user_logout

urlpatterns = [
    path('register/', register, name='register'),
    path('warning/', warning, name='warning'),
    path('profile/', profile_view, name='profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
