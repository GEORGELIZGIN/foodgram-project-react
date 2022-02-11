import csv

from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import pagination, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import CustomSearchFilter, RecipeFilter
from .models import (Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)
from .permissions import RecipePermissions
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipePartSerializer, RecipeSerializer,
                          TagSerializer)

CONTENT_TYPE = 'text/csv'
HEADERS = {
    'Content-Disposition': 'attachment; filename="somefilename.csv"'
}


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (CustomSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (RecipePermissions,)

    def get_queryset(self):

        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        is_favorited = self.request.query_params.get('is_favorited')

        res = Recipe.objects.all()
        user = self.request.user

        if is_in_shopping_cart is not None:

            if is_in_shopping_cart == '1':
                if user.is_anonymous:
                    return Recipe.objects.none()
                if ShoppingCart.objects.filter(user=user).exists():
                    res = res.intersection(user.shoppingcart.cart.all())
                else:
                    return Recipe.objects.none()

            elif is_in_shopping_cart == '0':
                if not user.is_anonymous:
                    if ShoppingCart.objects.filter(user=user).exists():
                        res = res.difference(user.shoppingcart.cart.all())

        if is_favorited is not None:
            if is_favorited == '1':
                if user.is_anonymous:
                    return Recipe.objects.none()
                if Favorite.objects.filter(user=user).exists():
                    res = res.intersection(user.favorite.favorite.all())
                else:
                    return Recipe.objects.none()
            elif is_favorited == '0':
                if not user.is_anonymous:
                    if Favorite.objects.filter(user=user).exists():
                        res = res.difference(user.favorite.favorite.all())
        return res

    filterset_class = RecipeFilter

    def _is_favorited_or_is_in_shopping_cart(self, request):

        if request.user.is_anonymous:
            is_favorited = False
            is_in_shopping_cart = False
            return {
                'is_favorited': is_favorited,
                'is_in_shopping_cart': is_in_shopping_cart
            }
        return {}

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self._is_favorited_or_is_in_shopping_cart(self.request))
        return context

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_destroy(self, recipe):
        recipe.ingredients.all().delete()
        recipe.delete()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shopping_list(request):
    response = HttpResponse(
        content_type=CONTENT_TYPE,
        headers=HEADERS,)
    if not ShoppingCart.objects.filter(user=request.user).exists():
        return response
    recipeids = Recipe.shoppingcart_set.through.objects.filter(
        shoppingcart__user=request.user).values_list('recipe', flat=True)
    res = Recipe.ingredients.through.objects.filter(
        recipe__id__in=recipeids).values(
            'ingredientwithamount__ingredient__name',
            'ingredientwithamount__ingredient__measurement_unit',).annotate(
                sum=Sum('ingredientwithamount__amount'))

    writer = csv.DictWriter(response, fieldnames=res[0].keys())
    writer.writerows(res)

    return response


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def add_delete_recipe_shopping_list(request, id):
    recipe = Recipe.objects.filter(id=id).first()
    if not recipe:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        shopping_cart, _ = ShoppingCart.objects.get_or_create(
            user=request.user)
        if ShoppingCart.objects.filter(
            user=request.user, cart=recipe
        ).exists():
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
    if not shopping_cart.cart.exists():
        shopping_cart.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def add_delete_favorite(request, id):
    recipe = Recipe.objects.filter(id=id).first()
    if not recipe:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        if Favorite.objects.filter(
            user=request.user,
            favorite=recipe
        ).first():
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        favorite, _ = Favorite.objects.get_or_create(user=request.user)
        favorite.favorite.add(recipe)
        return Response(
            status=status.HTTP_201_CREATED,
            data=RecipePartSerializer(
                recipe,
                context={'request': request}).data
        )
    favorite = Favorite.objects.filter(
        user=request.user,
        favorite=recipe
    ).first()
    if not favorite:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    favorite.favorite.remove(recipe)
    if not favorite.favorite.exists():
        favorite.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
