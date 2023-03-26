import datetime

from django import forms
from django.contrib.auth import get_user_model

from web.models import Note, Tag

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password', 'Пароли не совпадают')
        return cleaned_data

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class NoteForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = Note
        fields = ('title', 'text', 'image', 'tags')


class TagForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = Tag
        fields = ('name',)


class NoteFilterForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Поиск"}), required=False)
    start_date = forms.DateTimeField(
        label="От",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format='%Y-%m-%dT%H:%M'
        ),
        required=False
    )
    end_date = forms.DateTimeField(
        label="до",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format='%Y-%m-%dT%H:%M'
        ),
        required=False
    )


class ImportForm(forms.Form):
    file = forms.FileField()