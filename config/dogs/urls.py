from django.urls import path
from . import views

app_name = 'dogs'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.dogs_list, name='dogs_list'),
    path('dog/<int:dog_id>/', views.dog_detail, name='dog_detail'),
    path('breeds/', views.breeds_list, name='breeds'),
]