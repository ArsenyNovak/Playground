import os

from django.contrib.auth import get_user_model
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
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='playground', null=True, default=None)


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


def get_upload_to(instance, filename):
    return os.path.join('playground_photos', instance.playground.slug, filename)


class Photo(models.Model):
    playground = models.ForeignKey('Playground', on_delete=models.CASCADE, related_name='photo')
    image = models.ImageField(upload_to=get_upload_to, default=None,
                             null=True, verbose_name='Фотография')
    time_create = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


    def __str__(self):
        return self.image.url.split('/')[-1]


class Comment(models.Model):
    playground = models.ForeignKey('Playground', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='comments', null=True, default=None)
    time_create = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.playground}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create']
