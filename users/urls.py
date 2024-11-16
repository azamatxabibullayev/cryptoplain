from django.urls import path
from .views import register, warning, profile_view, user_login, user_logout, password_reset_confirm, \
    password_reset_request, UpdateProfileView, mobile_register, mobile_warning, mobile_profile_view, mobile_user_login, \
    mobile_password_reset_request, mobile_password_reset_confirm, mobile_user_logout, MobileUpdateProfileView
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
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('mobile/register/', mobile_register, name='mobile_register'),
    path('mobile/warning/', mobile_warning, name='mobile_warning'),
    path('mobile/profile/', mobile_profile_view, name='mobile_profile'),
    path('mobile/login/', mobile_user_login, name='mobile_login'),
    path('mobile/password_reset/', mobile_password_reset_request, name='mobile_password_reset'),
    path('mobile/reset/<uidb64>/<token>/', mobile_password_reset_confirm, name='mobile_password_reset_confirm'),
    path('mobile/logout/', mobile_user_logout, name='mobile_logout'),
    path('mobile/update_profile/', MobileUpdateProfileView.as_view(), name='mobile_update_profile'),
]
