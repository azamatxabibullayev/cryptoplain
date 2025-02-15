from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser, PremiumUser
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.translation import gettext_lazy as _


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            request.session['pending_user_id'] = user.id
            return redirect('warning')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def warning(request):
    if request.method == 'POST':
        if 'accept' in request.POST:
            user_id = request.session.pop('pending_user_id', None)
            if user_id:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=user_id)
                login(request, user)
                return redirect('profile')
        return redirect('register')
    return render(request, 'users/warning.html')


@login_required
def profile_view(request):
    user = request.user
    premium_user = None
    if hasattr(user, 'premium_user'):
        premium_user = user.premium_user

    context = {
        'user': user,
        'premium_user': premium_user,
        'user_id': user.id,
    }
    return render(request, 'users/profile.html', context)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            form.errors.clear()
            form.add_error(None, _("Foydalanuvchi nomi yoki paroli noto'g'ri kiritildi."))
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def handle_payment(user_id, premium_type):
    now = timezone.now()
    expired_users = PremiumUser.objects.filter(subscription_end__lt=now)
    for premium_user in expired_users:
        premium_user.delete()

    user = get_object_or_404(CustomUser, id=user_id)
    subscription_start = timezone.now()
    subscription_end = subscription_start + timedelta(days=30)
    premium_user, created = PremiumUser.objects.update_or_create(
        user=user,
        defaults={
            'premium_type': premium_type,
            'subscription_start': subscription_start,
            'subscription_end': subscription_end,
        }
    )
    return premium_user


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': 'kriptoindex.uz',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def password_reset_confirm(request, uidb64=None, token=None):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'users/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'users/password_reset_invalid.html')


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        context = {
            'form': update_form
        }
        return render(request, 'users/update_profile.html', context=context)

    def post(self, request):
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('profile')
        else:
            context = {
                'form': update_form
            }
            return render(request, 'users/update_profile.html', context=context)


# MOBILE MODE

def mobile_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            request.session['pending_user_id'] = user.id
            return redirect('mobile_warning')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register_mobile.html', {'form': form})


def mobile_warning(request):
    if request.method == 'POST':
        if 'accept' in request.POST:
            user_id = request.session.pop('pending_user_id', None)
            if user_id:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=user_id)
                login(request, user)
                return redirect('mobile_profile')
        return redirect('mobile_register')
    return render(request, 'users/warning_mobile.html')


def mobile_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('mobile_login')

    user = request.user
    premium_user = None
    if hasattr(user, 'premium_user'):
        premium_user = user.premium_user

    context = {
        'user': user,
        'premium_user': premium_user,
        'user_id': user.id,
    }
    return render(request, 'users/profile_mobile.html', context)


def mobile_user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mobile_profile')
        else:
            form.errors.clear()
            form.add_error(None, _("Foydalanuvchi nomi yoki paroli noto'g'ri kiritildi."))
    else:
        form = AuthenticationForm()
    return render(request, 'users/login_mobile.html', {'form': form})


def mobile_password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password_reset_email_mobile.html"
                    c = {
                        "email": user.email,
                        'domain': 'kriptoindex.uz',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            return redirect("password_reset_done_mobile")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password_reset_mobile.html",
                  context={"password_reset_form": password_reset_form})


def mobile_password_reset_confirm(request, uidb64=None, token=None):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete_mobile')
        else:
            form = SetPasswordForm(user)
        return render(request, 'users/password_reset_confirm_mobile.html', {'form': form})
    else:
        return render(request, 'users/password_reset_invalid_mobile.html')


def mobile_user_logout(request):
    logout(request)
    return redirect('mobile_login')


class MobileUpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        context = {
            'form': update_form
        }
        return render(request, 'users/update_profile_mobile.html', context=context)

    def post(self, request):
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('mobile_profile')
        else:
            context = {
                'form': update_form
            }
            return render(request, 'users/update_profile_mobile.html', context=context)
