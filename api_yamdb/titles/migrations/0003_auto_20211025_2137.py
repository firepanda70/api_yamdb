# Generated by Django 2.2.16 on 2021-10-25 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0002_remove_title_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catergory',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('name',), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(db_index=True, error_messages={'MaxValueValidator': 'Треки не должны быть из будущего', 'MinValueValidator': 'Записи не должны быть старше 19 века'}, verbose_name='Год Выпуска'),
        ),
    ]
