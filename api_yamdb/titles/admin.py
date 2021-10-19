from django.contrib import admin

from .models import Catergory, Genre, Title

EMPTY = '-пусто-'


@admin.register(Catergory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'pk')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'pk')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY


@admin.register(Title)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
        'pk'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY

