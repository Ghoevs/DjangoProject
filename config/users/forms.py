from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, AuthenticationForm
from .models import User
from .validators import password_validator
from dogs.mixins import StyleFormMixin


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Минимум 8 символов, заглавная и строчная буква, цифра'


class CustomAuthenticationForm(StyleFormMixin, AuthenticationForm):
    """Форма входа с email вместо username"""
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))


class CustomPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    pass


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass


class CustomSetPasswordForm(StyleFormMixin, SetPasswordForm):
    pass