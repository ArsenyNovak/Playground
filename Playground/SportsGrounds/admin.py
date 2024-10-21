from django.contrib import admin

from SportsGrounds.models import Category, Playground, Photo, Comment


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Playground)
class PlaygroundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description', 'time_update')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Photo)
class Photo(admin.ModelAdmin):
    list_display = ('id', 'image', 'playground', 'time_create')

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('id', 'playground', 'text', 'author', 'time_create')