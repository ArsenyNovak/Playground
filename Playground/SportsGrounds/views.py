from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

from django.shortcuts import render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPlayGroundForm, LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, \
    UserPasswordResetForm, UserSetPasswordForm
from .models import Category, Playground, Photo


# Create your views here.

class HomePage(ListView):
    model = Category
    template_name = 'SportsGrounds/index.html'
    extra_context = {'title': 'Главная страница'}
    context_object_name = 'categories'


class About(TemplateView):
    template_name = 'SportsGrounds/about.html'
    title_page = 'О сайте'
    extra_context = {'title': 'О сайте'}


class ShowCategory(ListView):
    template_name = 'SportsGrounds/show_category.html'
    context_object_name = 'playgrounds'
    allow_empty = False
    paginate_by = 5


    def get_queryset(self):
        return Playground.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = Category.objects.filter(slug=self.kwargs['cat_slug'])
        context["cat"] = cat[0].name
        return context


class ShowSportGround(DetailView):
    model = Playground
    template_name = 'SportsGrounds/show_SportsGrounds.html'
    context_object_name = 'playground'
    slug_url_kwarg = 'sportground_slug'


class AllPlayGrounds(ListView):

    template_name = 'SportsGrounds/show_category.html'
    context_object_name = 'playgrounds'
    allow_empty = False

    def get_queryset(self):
        return Playground.objects.filter(is_published=True)



class AddPlayGrounds(LoginRequiredMixin, FormView):
    template_name = 'SportsGrounds/add_sportground.html'
    form_class = AddPlayGroundForm
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Добавление площадки'}


    def form_valid(self, form):

        files = form.cleaned_data["photo_all"]
        pg = Playground(name=form.cleaned_data["name"],
                        description=form.cleaned_data["description"],
                        author=self.request.user
        )
        pg.save()
        for f in files:
            fp = Photo(image=f, playground=pg)
            fp.save()
        pg.cat.add(*form.cleaned_data["cat"])
        pg.save()
        return super().form_valid(form)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'SportsGrounds/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterCreateUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'SportsGrounds/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = 'SportsGrounds/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "SportsGrounds/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}

class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    success_url = reverse_lazy("password_reset_done")
    template_name = "SportsGrounds/password_reset_form.html"
    extra_context = {'title': "Восстановление пароля"}

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name = "SportsGrounds/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")
    extra_context = {'title': "Новый пороль"}
