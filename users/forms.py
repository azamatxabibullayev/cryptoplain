from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, PremiumUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Parol"),
        widget=forms.PasswordInput,
        help_text=_("Parol uchun minimum uzunlik 8 tani tashkil qiladi."),
    )
    password2 = forms.CharField(
        label=_("Parolni tasdiqlang"),
        widget=forms.PasswordInput,
        help_text=_("Parollar mos bo'lishi kerak."),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'surname', 'profile_pic')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            self.add_error("username", _("Bu foydalanuvchi nomi band. Iltimos, boshqa nom tanlang."))
        email = cleaned_data.get("email")
        if email and CustomUser.objects.filter(email=email).exists():
            self.add_error("email", _("Bu email ro'yxatdan o'tilgan. Iltimos, boshqa email manzilini kiriting."))
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and len(password1) < 8:
            self.add_error("password1", _("Parol uchun minimum uzunlik 8 tani tashkil qiladi."))
        if password1 and password2 and password1 != password2:
            self.add_error("password2", _("Parollar mos emas."))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


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
        fields = ('username', 'email', 'name', 'surname', 'profile_pic')
