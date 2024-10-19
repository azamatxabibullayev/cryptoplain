from django import forms
from .models import Note
from django.utils.translation import gettext_lazy as _


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Zametka nomi'), 'class': 'note-name-input'}),
            'content': forms.Textarea(attrs={'placeholder': _('Zametka'), 'class': 'note-content'}),
        }
