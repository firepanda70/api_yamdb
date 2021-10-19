import textwrap

from django.db import models
from django.contrib.auth import get_user_model

from titles.models import Title
from .validators import score_validation

User = get_user_model()


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Отзыв на произведение'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Автор отзыва'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        help_text='Дата публикации отзыва'
    )
    score = models.IntegerField(
        'Оценка',
        help_text='Оценка пользователя',
        validators=(score_validation,)
    )
    text = models.TextField('Текст', help_text='Текст поста')

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        fullname = self.author.get_full_name()
        slug = self.author.username
        res = f'Отзыв пользователя {fullname} ({slug})\n'
        shorten_text = textwrap.shorten(
            text=self.text,
            width=30,
            placeholder='...'
        )
        res += f'Текст: {shorten_text}\n'
        res += self.pub_date.strftime('%b %d, %Y, %H:%M')
        return res


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Комментарии к отзыву'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        help_text='Дата добавления комментария'
    )
    text = models.TextField('Текст', help_text='Текст комментария')

    class Meta():
        ordering = ('pub_date', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        fullname = self.author.get_full_name()
        slug = self.author.username
        res = f'Комментарий пользователя {fullname} ({slug})\n'
        res += f'Текст: {self.text}\n'
        res += self.pub_date.strftime('%b %d, %Y, %H:%M')
        return res
