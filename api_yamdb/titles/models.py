from django.db import models

ERROR_MESSAGES = {'MinValueValidator': 'Записи не должны быть старше 19 века',
                  'MaxValueValidator': 'Треки не должны быть из будущего'}


class Catergory(models.Model):
    name = models.CharField('Имя Категории', max_length=100)
    slug = models.SlugField('Слаг Категории', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField('Имя Жанра', max_length=100)
    slug = models.SlugField('Слаг Жанра', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}'


class Title(models.Model):
    name = models.CharField('Имя Произведения', max_length=200)
    year = models.PositiveSmallIntegerField('Год Выпуска',
                                            db_index=True,
                                            error_messages=ERROR_MESSAGES)
    description = models.TextField(
        'Описание Произведения',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр Произведения',
    )
    category = models.ForeignKey(
        Catergory,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория Произведения',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name} {self.year}'
