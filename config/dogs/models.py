from django.db import models


class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название породы')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'

    def __str__(self):
        return self.name


class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Кличка')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='dogs', verbose_name='Порода')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст (лет)')
    photo = models.ImageField(upload_to='dogs/', blank=True, null=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'

    def __str__(self):
        return f'{self.name} ({self.breed.name})'