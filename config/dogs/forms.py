from django import forms
from .models import Dog, Pedigree, Review
from .mixins import StyleFormMixin


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


class DogFullForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'age', 'photo', 'description', 'is_active', 'owner']


class PedigreeForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Pedigree
        fields = ['father', 'mother', 'grandfather_father', 'grandmother_father',
                  'grandfather_mother', 'grandmother_mother', 'awards']


class ReviewForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш отзыв...'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }