from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

from django.urls import reverse_lazy
from django.views.generic import  CreateView, UpdateView

from .forms import  LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, \
    UserPasswordResetForm, UserSetPasswordForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'User/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterCreateUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'User/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('user:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = 'User/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("user:password_change_done")
    template_name = "User/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}

class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    success_url = reverse_lazy("user:password_reset_done")
    template_name = "User/password_reset_form.html"
    extra_context = {'title': "Восстановление пароля"}
    email_template_name = "User/password_reset_email.html"

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name = "User/password_reset_confirm.html"
    success_url = reverse_lazy("user:password_reset_complete")
    extra_context = {'title': "Новый пороль"}