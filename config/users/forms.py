from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
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


class CustomPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = 'Минимум 8 символов, заглавная и строчная буква, цифра'


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass


class CustomSetPasswordForm(StyleFormMixin, SetPasswordForm):
    pass