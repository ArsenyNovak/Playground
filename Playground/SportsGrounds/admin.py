from django.contrib import admin

from SportsGrounds.models import Category, Playground


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')

@admin.register(Playground)
class PlaygroundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    list_display_links = ('id', 'name')