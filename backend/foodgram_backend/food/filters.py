import django_filters
from rest_framework import filters

from food.models import Recipe


class CustomSearchFilter(filters.SearchFilter):
    search_param = 'name'


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact')

    class Meta:
        model = Recipe
        fields = ('author',)
