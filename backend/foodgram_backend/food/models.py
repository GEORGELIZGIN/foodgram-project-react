from django.contrib.auth import get_user_model
from django.db import models
from food.validators import validate_tag_color

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='автор')
    name = models.CharField(
        max_length=200,
        verbose_name='название',
        help_text='название рецепта')
    text = models.TextField(
        verbose_name='описание',
        help_text='текстовое описание рецепта')
    cooking_time = models.PositiveIntegerField(
        verbose_name='время готовки',
        help_text='время готовки в минутах')
    ingredients = models.ManyToManyField(
        'IngredientWithAmount',
        verbose_name='ингридиенты',
        help_text='ингридиенты и их количество')
    image = models.ImageField(
        upload_to='images/',
        verbose_name='картинка',
        help_text='картинка')
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='тэги',
        help_text='тэги поиска рецептов')

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='ингридиент',
        help_text='название ингридиента')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='единица измерения',
        help_text='произвольная единица измерения')

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='тэг',
        help_text='название тэга')
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name='цвет',
        help_text='цвет в формате HEX',
        validators=(validate_tag_color,))
    slug = models.SlugField(
        max_length=200, null=True,
        verbose_name='слаг', help_text='слаг')

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.name


class IngredientWithAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='ингридиент с количеством',)
    amount = models.PositiveSmallIntegerField(verbose_name='количество')

    class Meta:
        verbose_name = 'ингридиент с количеством'
        verbose_name_plural = 'ингридиенты с количеством'

    def __str__(self):
        return f'ингридиент: {self.ingredient.name} количество: {self.amount}'


class Favorite(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name='пользователь')
    favorite = models.ManyToManyField(Recipe, verbose_name='избранное')

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'

    def __str__(self):
        return f'избранное пользователя {self.user}'


class ShoppingCart(models.Model):
    cart = models.ManyToManyField(Recipe, verbose_name='корзина')
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        unique=True, verbose_name='пользователь')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзина'

    def __str__(self):
        return f'корзина пользователя {self.user}'
