import django_filters
from rest_framework import filters

from .models import Recipe


class CustomSearchFilter(filters.SearchFilter):
    search_param = 'name'


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='contains')
    author = django_filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
