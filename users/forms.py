from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, PremiumUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'surname', 'profile_pic')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'surname', 'profile_pic',)


class PremiumUserForm(forms.ModelForm):
    class Meta:
        model = PremiumUser
        fields = ['user', 'premium_type', 'subscription_start', 'subscription_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
