from django.urls import path
from . import views

app_name = 'dogs'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.dogs_list, name='dogs_list'),
    path('dog/<int:dog_id>/', views.dog_detail, name='dog_detail'),
    path('create/', views.dog_create, name='dog_create'),
    path('dog/<int:dog_id>/update/', views.dog_update, name='dog_update'),
    path('dog/<int:dog_id>/delete/', views.dog_delete, name='dog_delete'),
    path('breeds/', views.breeds_list, name='breeds'),
]