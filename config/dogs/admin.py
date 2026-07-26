from django.contrib import admin
from .models import Breed, Dog


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'created_at')
    list_filter = ('breed', 'age')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)