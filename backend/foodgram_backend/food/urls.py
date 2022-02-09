from django.urls import path
from rest_framework import routers

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    add_delete_favourite, add_delete_recipe_shopping_list,
                    get_shopping_list)

router = routers.SimpleRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
urlpatterns = [
    path('recipes/download_shopping_cart/', get_shopping_list),
    path('recipes/<int:id>/shopping_cart/', add_delete_recipe_shopping_list),
    path('recipes/<int:id>/favourite/', add_delete_favourite),
]
urlpatterns += router.urls
