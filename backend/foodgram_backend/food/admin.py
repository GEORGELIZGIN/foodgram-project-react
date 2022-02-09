from django.contrib import admin

from . import models


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('name', 'author', 'tags')


class IngredientWithAmountAdmin(admin.ModelAdmin):
    pass


class FavouriteAdmin(admin.ModelAdmin):
    pass


class ShoppingCartAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.IngredientWithAmount, IngredientWithAmountAdmin)
admin.site.register(models.Favourite, FavouriteAdmin)
admin.site.register(models.ShoppingCart, ShoppingCartAdmin)
