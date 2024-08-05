from django.urls import path
from .views import register, warning, profile_view, user_login, user_logout, password_reset_confirm, \
    password_reset_request
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', register, name='register'),
    path('warning/', warning, name='warning'),
    path('profile/', profile_view, name='profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password_reset/done/', TemplateView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/done/', TemplateView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
