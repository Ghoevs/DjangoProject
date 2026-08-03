from django import forms
from .models import Dog
from .mixins import StyleFormMixin
from django.core.validators import MinValueValidator, MaxValueValidator


class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'age', 'photo', 'description']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 0:
            raise forms.ValidationError('Возраст не может быть отрицательным')
        if age > 30:
            raise forms.ValidationError('Собаки столько не живут')
        return age

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Кличка должна быть не менее 2 символов')
        return name