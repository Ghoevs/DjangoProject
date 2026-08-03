from django.core.exceptions import ValidationError
import re


def password_validator(value):
    if len(value) < 8:
        raise ValidationError('Пароль должен быть не менее 8 символов')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
    if not re.search(r'[a-z]', value):
        raise ValidationError('Пароль должен содержать хотя бы одну строчную букву')
    if not re.search(r'\d', value):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру')