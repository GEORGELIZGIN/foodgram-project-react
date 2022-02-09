from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)

    objects = UserManager()

    REQUIRED_FIELDS = ('first_name', 'last_name', 'email',)


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='followings',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('follower', 'author'),
                name='follow_constraint'),
        )

    def __str__(self):
        return f'{self.follower} подписан на {self.author}'
