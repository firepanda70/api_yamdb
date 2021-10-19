from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    UserRoles = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )

    role = models.CharField(choices=UserRoles,
                            default='user',
                            max_length=9,
                            verbose_name='Тип пользователя')
    email = models.EmailField(verbose_name='e-mail', unique=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
