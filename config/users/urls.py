from django.urls import path
from . import views
from .forms import CustomAuthenticationForm

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('all/', views.UserListView.as_view(), name='user_list'),
    path('<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
]