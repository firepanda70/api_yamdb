from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE_LENGTH_ERROR = 'Превышена длинна роли пользователя'


class User(AbstractUser):
    UserRoles = (
        ('anonymous', 'Анонимный'),
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )

    role = models.CharField(choices=UserRoles,
                            default='user',
                            max_length=16,
                            verbose_name='Тип пользователя',
                            error_messages={
                                'max_length': USER_ROLE_LENGTH_ERROR
                            })
    email = models.EmailField(verbose_name='e-mail', unique=True)
    bio = models.TextField(default='', verbose_name='Описание пользователя')

    @property
    def is_anonymous(self):
        return self.role == 'anonymous'

    class Meta:
        ordering = ('id',)
