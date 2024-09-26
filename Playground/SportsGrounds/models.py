from django.db import models
from django.urls import reverse


# Create your models here.
class Playground(models.Model):
    name = models.CharField(max_length=50, verbose_name= 'Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name= 'слаг')
    description = models.TextField(verbose_name= 'Описание')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    cat = models.ManyToManyField('Category', related_name='cat', verbose_name= 'Площадки')
    photo = models.ManyToManyField('Photo', blank=True, related_name='Photo', verbose_name= 'Фото')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
       return reverse('sport_ground', kwargs={'sportground_slug': self.slug})

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name= 'слаг')
    image = models.ImageField(upload_to='category_photo/', default=None,
                             null=True, verbose_name='Картинка')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class Photo(models.Model):
    image = models.ImageField(upload_to='playground_photos/', default=None,
                             null=True, verbose_name='Фотография')

    def __str__(self):
        return self.image.url.split('/')[-1]