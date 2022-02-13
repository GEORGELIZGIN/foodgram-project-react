from django.contrib import admin

from food.models import (Favorite, Ingredient, IngredientWithAmount, Recipe,
                         ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('slug',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('name', 'measurement_unit')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'fav', 'cart')
    list_filter = ('author__email', 'tags__slug')
    search_fields = (
        'author__email', 'author__username',
        'author__first_name', 'author__last_name',
        'ingredients__ingredient__name')

    @admin.display(description='Число добавлений в избранное')
    def fav(self, obj):
        cn = Favorite.objects.filter(favorite=obj).count()
        return cn

    @admin.display(description='Число добавлений в корзину')
    def cart(self, obj):
        cn = ShoppingCart.objects.filter(cart=obj).count()
        return cn


class IngredientWithAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'amount')
    search_fields = ('ingredient__name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = (
        'user__email', 'user__username',
        'user__first_name', 'user__last_name')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = (
        'user__email', 'user__username',
        'user__first_name', 'user__last_name',
        'cart__name')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientWithAmount, IngredientWithAmountAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
