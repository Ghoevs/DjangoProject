from django.contrib import admin
from .models import Breed, Dog, Pedigree


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'owner', 'created_at')
    list_filter = ('breed', 'age')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


@admin.register(Pedigree)
class PedigreeAdmin(admin.ModelAdmin):
    list_display = ('dog', 'father', 'mother', 'created_at')
    search_fields = ('dog__name', 'father', 'mother')