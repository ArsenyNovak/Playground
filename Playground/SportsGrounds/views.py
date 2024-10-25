from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured

from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, FormView
from django.views.generic.edit import FormMixin

from .forms import AddPlayGroundForm, AddCommentForm
from .models import Category, Playground, Photo, Comment


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



