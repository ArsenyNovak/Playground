from django.db import models
from django.urls import reverse
from pytils.translit import slugify


# Create your models here.
class Playground(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'


    name = models.CharField(max_length=50, verbose_name= 'Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name= 'слаг')
    description = models.TextField(verbose_name= 'Описание')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    cat = models.ManyToManyField('Category', related_name='cat', verbose_name= 'Площадки')


    class Meta:
        verbose_name = 'Спортивная площадка'
        verbose_name_plural = 'Спортивные площадки'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
       return reverse('sport_ground', kwargs={'sportground_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Playground, self).save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name= 'слаг')
    image = models.ImageField(upload_to='category_photo/', default=None,
                             null=True, verbose_name='Картинка')

    class Meta:
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class Photo(models.Model):
    playground = models.ForeignKey('Playground', on_delete=models.CASCADE, related_name='photo')
    image = models.ImageField(upload_to='playground_photos/', default=None,
                             null=True, verbose_name='Фотография')
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

