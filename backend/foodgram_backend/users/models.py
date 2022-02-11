from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150, blank=False,
        verbose_name='имя')
    last_name = models.CharField(
        max_length=150, blank=False,
        verbose_name='фамилия')
    password = models.CharField(
        max_length=150, verbose_name='пароль')
    email = models.EmailField(
        max_length=254, unique=True,
        verbose_name='email')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('first_name', 'last_name', 'username',)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='followings',
        on_delete=models.CASCADE,
        verbose_name='подписчик')
    author = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
        verbose_name='автор')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('follower', 'author'),
                name='follow_constraint'),
        )

    def __str__(self):
        return f'{self.follower} подписан на {self.author}'
