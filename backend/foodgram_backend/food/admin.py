from django.contrib import admin

from . import models


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class RecipeAdmin(admin.ModelAdmin):
    pass


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
