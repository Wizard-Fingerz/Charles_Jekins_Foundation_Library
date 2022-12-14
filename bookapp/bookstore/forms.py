from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.forms import ModelForm
from bookstore.models import Chat, Book, Profile
from django import forms


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('message', )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'year', 'uploaded_by', 'desc')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']