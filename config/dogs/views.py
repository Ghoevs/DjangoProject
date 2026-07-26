from django.shortcuts import render, get_object_or_404
from .models import Dog, Breed


def index(request):
    return render(request, 'dogs/index.html')


def dogs_list(request):
    dogs = Dog.objects.all().order_by('-created_at')
    return render(request, 'dogs/dogs_list.html', {'dogs': dogs})


def dog_detail(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    return render(request, 'dogs/detail.html', {'dog': dog})


def breeds_list(request):
    breeds = Breed.objects.all()
    return render(request, 'dogs/breeds.html', {'breeds': breeds})