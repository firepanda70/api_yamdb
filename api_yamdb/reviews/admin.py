from django.contrib import admin

from .models import Review, Comment

EMPTY = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'score', 'text')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = EMPTY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'pub_date', 'text')
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = EMPTY
