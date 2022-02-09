from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()
    ingredients = models.ManyToManyField('IngredientWithAmount')
    image = models.ImageField()
    tags = models.ManyToManyField('Tag')


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, null=True)
    slug = models.SlugField(max_length=200, null=True)


class IngredientWithAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


class Favourite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    favourite = models.ManyToManyField(Recipe)


class ShoppingCart(models.Model):
    cart = models.ManyToManyField(Recipe)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
