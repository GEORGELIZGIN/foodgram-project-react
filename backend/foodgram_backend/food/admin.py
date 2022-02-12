from django.contrib import admin

from food.models import (Favorite, Ingredient, IngredientWithAmount, Recipe,
                         ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('slug',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'fav', 'cart')
    list_filter = ('author', 'tags__slug')
    search_fields = ('author__username', 'ingredients__ingredient__name')

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
    list_filter = ('ingredient',)
    search_fields = ('ingredient__name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientWithAmount, IngredientWithAmountAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
