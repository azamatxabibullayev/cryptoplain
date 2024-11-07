from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, PremiumUser
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'surname', 'profile_pic')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'surname', 'profile_pic', 'user_type')


class PremiumUserForm(forms.ModelForm):
    class Meta:
        model = PremiumUser
        fields = ['user', 'premium_type', 'subscription_start', 'subscription_end']

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if not CustomUser.objects.filter(id=user.id).exists():
            raise forms.ValidationError('Selected user does not exist.')
        return user


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'reset-input',
            'placeholder': _('Foydalanuvchi email'),
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_pic')
