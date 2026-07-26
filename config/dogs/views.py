from django.shortcuts import render, get_object_or_404, redirect
from .models import Dog, Breed
from .forms import DogForm


def index(request):
    return render(request, 'dogs/index.html')


def dogs_list(request):
    dogs = Dog.objects.all().order_by('-created_at')
    return render(request, 'dogs/dogs_list.html', {'dogs': dogs})


def dog_detail(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    return render(request, 'dogs/detail.html', {'dog': dog})


def dog_create(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dogs:dogs_list')
    else:
        form = DogForm()
    return render(request, 'dogs/dog_form.html', {'form': form, 'action': 'Добавить'})


def dog_update(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            return redirect('dogs:dog_detail', dog_id=dog.id)
    else:
        form = DogForm(instance=dog)
    return render(request, 'dogs/dog_form.html', {'form': form, 'action': 'Изменить'})


def dog_delete(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    if request.method == 'POST':
        dog.delete()
        return redirect('dogs:dogs_list')
    return render(request, 'dogs/dog_confirm_delete.html', {'dog': dog})


def breeds_list(request):
    breeds = Breed.objects.all()
    return render(request, 'dogs/breeds.html', {'breeds': breeds})