from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, FormView

from .forms import AddPlayGroundForm
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



