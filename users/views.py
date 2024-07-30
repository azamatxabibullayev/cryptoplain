from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, PremiumUserForm
from .models import CustomUser, PremiumUser


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            request.session['user_data'] = form.cleaned_data  # Save form data in session
            return redirect('warning')  # Redirect to warning page
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def warning(request):
    if request.method == 'POST':
        if 'accept' in request.POST:
            # Retrieve user data from session and create user
            user_data = request.session.pop('user_data', None)
            if user_data:
                form = CustomUserCreationForm(user_data)
                user = form.save()
                login(request, user)
                return redirect('profile')
        return redirect('register')  # Redirect back to register if declined
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
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def handle_payment(user_id, premium_type):
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
