from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Dog, Breed, Pedigree
from .forms import DogForm, DogFullForm, PedigreeForm
from .services import send_views_notification
from users.services import send_dog_created_email


class IndexView(TemplateView):
    template_name = 'dogs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Питомник собак'
        return context


class DogListView(ListView):
    model = Dog
    template_name = 'dogs/dogs_list.html'
    context_object_name = 'dogs'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'
    context_object_name = 'dog'
    pk_url_kwarg = 'dog_id'

    def get_object(self, queryset=None):
        dog = super().get_object(queryset)
        if self.request.user != dog.owner:
            dog.views += 1
            dog.save()
            send_views_notification(dog)
        return dog


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    success_url = reverse_lazy('dogs:dogs_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Добавить'
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        send_dog_created_email(self.request.user, self.object)
        messages.success(self.request, 'Собака добавлена!')
        return response


class DogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Dog
    template_name = 'dogs/dog_form.html'
    pk_url_kwarg = 'dog_id'

    def test_func(self):
        dog = self.get_object()
        return self.request.user == dog.owner or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на редактирование этой собаки')
        return redirect('dogs:dogs_list')

    def get_form_class(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return DogFullForm
        return DogForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Изменить'
        return context

    def get_success_url(self):
        return reverse_lazy('dogs:dog_detail', kwargs={'dog_id': self.object.id})


class DogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dog
    template_name = 'dogs/dog_confirm_delete.html'
    pk_url_kwarg = 'dog_id'
    success_url = reverse_lazy('dogs:dogs_list')

    def test_func(self):
        dog = self.get_object()
        return self.request.user == dog.owner or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на удаление этой собаки')
        return redirect('dogs:dogs_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Собака удалена!')
        return super().delete(request, *args, **kwargs)


class BreedListView(ListView):
    model = Breed
    template_name = 'dogs/breeds.html'
    context_object_name = 'breeds'


class PedigreeCreateView(LoginRequiredMixin, CreateView):
    model = Pedigree
    form_class = PedigreeForm
    template_name = 'dogs/pedigree_form.html'
    success_url = reverse_lazy('dogs:dogs_list')

    def form_valid(self, form):
        dog = get_object_or_404(Dog, id=self.kwargs['dog_id'])
        form.instance.dog = dog
        messages.success(self.request, f'Родословная для {dog.name} добавлена!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dog'] = get_object_or_404(Dog, id=self.kwargs['dog_id'])
        return context


class PedigreeDetailView(DetailView):
    model = Pedigree
    template_name = 'dogs/pedigree_detail.html'
    context_object_name = 'pedigree'

    def get_object(self):
        dog = get_object_or_404(Dog, id=self.kwargs['dog_id'])
        return get_object_or_404(Pedigree, dog=dog)