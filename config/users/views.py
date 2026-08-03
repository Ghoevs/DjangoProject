from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import (
    PasswordChangeView, PasswordResetView, PasswordResetConfirmView
)
from django.urls import reverse_lazy
from .forms import (
    CustomUserCreationForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm
)
from .services import send_welcome_email


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_welcome_email(user)  # отправка письма
            messages.success(request, 'Регистрация прошла успешно! Проверьте почту.')
            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Неверный email или пароль')
    return render(request, 'users/login.html')


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})


def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('dogs:index')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        from .services import send_password_change_email
        update_session_auth_hash(self.request, form.user)
        send_password_change_email(self.request.user)
        messages.success(self.request, 'Пароль успешно изменен!')
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:login')
    email_template_name = 'users/password_reset_email.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')