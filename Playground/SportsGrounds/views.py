from urllib.parse import urlparse

from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import resolve_url

from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, FormView
from django.views.generic.edit import FormMixin
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .forms import AddPlayGroundForm, AddCommentForm
from .models import Category, Playground, Photo, Comment
from .serializers import PlaygroundSerializer, CategorySerializer


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
    paginate_by = 3


    def get_queryset(self):
        return Playground.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = Category.objects.filter(slug=self.kwargs['cat_slug'])
        context["cat"] = cat[0].name
        context["title"] = cat[0].name
        return context


class ShowSportGround(DetailView, FormMixin):
    model = Playground
    form_class = AddCommentForm
    template_name = 'SportsGrounds/show_SportsGrounds.html'
    context_object_name = 'playground'
    slug_url_kwarg = 'sportground_slug'
    extra_context = {'title': 'Просмотр площадки'}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        com = Comment(playground=Playground.objects.get(slug=self.kwargs["sportground_slug"]),
                      text=form.cleaned_data["text"],
                      author=self.request.user
        )
        com.save()
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy('sport_ground', args=[self.kwargs['sportground_slug']])
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)


class AllPlayGrounds(ListView):

    template_name = 'SportsGrounds/show_category.html'
    context_object_name = 'playgrounds'
    allow_empty = False
    extra_context = {'title': 'Все площадки'}
    paginate_by = 3

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


class APIList(AccessMixin, TemplateView):
    template_name = 'SportsGrounds/API.html'
    title_page = 'API'
    extra_context = {'title': 'API'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = self.request.get_host
        return context

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated & request.user.is_staff):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.raise_exception or (self.request.user.is_authenticated & self.request.user.is_staff):
            raise PermissionDenied(self.get_permission_denied_message())

        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


class CategoryApiList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PlaygroundPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class PlayGroundsApi(ListAPIView):
    serializer_class = PlaygroundSerializer
    pagination_class = PlaygroundPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        slug = self.kwargs['cat_slug']
        if slug != 'all':
            return Playground.objects.filter(cat__slug=slug, is_published=True)
        return Playground.objects.filter(is_published=True)


class PlaygroundsApiDetail(ListAPIView):
    serializer_class = PlaygroundSerializer

    def get_queryset(self):
        return Playground.objects.filter(slug=self.kwargs["sportground_slug"])