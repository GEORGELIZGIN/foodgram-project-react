import csv

import django_filters
from django.http import HttpResponse
from rest_framework import filters, pagination, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favourite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import RecipePermissions
from .serializers import (
    IngredientSerializer, RecipeCreateSerializer, RecipeSerializer,
    TagSerializer, RecipePartSerializer,
    RecipeCreateSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CustomSearchFilter(filters.SearchFilter):
    search_param = "name"


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='contains')
    author = django_filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact')

    class Meta:
        model = Recipe
        fields = ['tags', 'author']


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (CustomSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (RecipePermissions,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeCreateSerializer
        return RecipeSerializer

    def destroy(self, request, *args, **kwargs):
        print(request.body)
        print('aaaa')
        print(self)
        recipe = self.get_object()
        print(recipe)
        recipe.ingredients.all().delete()
        self.perform_destroy(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shopping_list(request):
    print(request.user)
    response = HttpResponse(
        content_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )
    shopping_cart = ShoppingCart.objects.filter(user=request.user).first()
    if not shopping_cart:
        return response
    recipes = shopping_cart.cart.all()
    dict_of_ingredients = {}
    for recipe in recipes.all():
        for ingredient_with_amount in recipe.ingredients.all():
            if ingredient_with_amount.ingredient.name in dict_of_ingredients:
                dict_of_ingredients[
                    ingredient_with_amount.ingredient.name
                ]['amount'] += ingredient_with_amount.amount
            else:
                dict_of_ingredients[ingredient_with_amount.ingredient.name] = {
                    'amount': ingredient_with_amount.amount,
                    'measurement_unit': (
                        ingredient_with_amount.ingredient.measurement_unit),
                }

    writer = csv.writer(response)
    for ingredient_name in dict_of_ingredients:
        writer.writerow(
            [
                ingredient_name,
                dict_of_ingredients[ingredient_name]['amount'],
                dict_of_ingredients[ingredient_name]['measurement_unit']
            ])

    return response


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def add_delete_recipe_shopping_list(request, id):
    recipe = Recipe.objects.filter(id=id).first()
    if not recipe:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        shopping_cart = ShoppingCart.objects.filter(user=request.user).first()
        if not shopping_cart:
            shopping_cart = ShoppingCart.objects.create(user=request.user)
        if ShoppingCart.objects.filter(user=request.user, cart=recipe).first():
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        shopping_cart.cart.add(recipe)
        return Response(
            status=status.HTTP_201_CREATED,
            data=RecipePartSerializer(
                recipe,
                context={'request': request}).data
        )
    shopping_cart = ShoppingCart.objects.filter(
        user=request.user,
        cart=recipe
    ).first()
    if not shopping_cart:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    shopping_cart.cart.remove(recipe)
    if len(shopping_cart.cart.all()) == 0:
        shopping_cart.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def add_delete_favourite(request, id):
    recipe = Recipe.objects.filter(id=id).first()
    if not recipe:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        favourite = Favourite.objects.filter(user=request.user).first()
        if not favourite:
            favourite = Favourite.objects.create(user=request.user)
        if Favourite.objects.filter(
            user=request.user,
            favourite=recipe
        ).first():
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        favourite.favourite.add(recipe)
        return Response(
            status=status.HTTP_201_CREATED,
            data=RecipePartSerializer(
                recipe,
                context={'request': request}).data
        )
    favourite = Favourite.objects.filter(
        user=request.user,
        favourite=recipe
    ).first()
    if not favourite:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    favourite.favourite.remove(recipe)
    if len(favourite.favourite.all()) == 0:
        favourite.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
