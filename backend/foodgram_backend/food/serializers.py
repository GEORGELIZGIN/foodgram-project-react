from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework import validators

from users.serializers import UserSerializer

from .models import (Favourite, Ingredient, IngredientWithAmount, Recipe,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientWithAmountSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientWithAmount
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientWithAmountSerializer(many=True)
    tags = TagSerializer(many=True)
    is_favourite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favourite(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        favourit = Favourite.objects.filter(
            user=self.context['request'].user,
            favourite=obj)
        if len(favourit) == 0:
            return False
        return True

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        favourit = ShoppingCart.objects.filter(
            user=self.context['request'].user,
            cart=obj)
        if len(favourit) == 0:
            return False
        return True


class CreateIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientWithAmount
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='id',
        queryset=Tag.objects.all())
    ingredients = CreateIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags',
            'name', 'text',
            'cooking_time', 'image')

    def create(self, validated_data):
        print(validated_data)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        if not ingredients:
            raise validators.ValidationError(
                'list of ingredients cannot be empty')
        recipe = Recipe.objects.create(
            name=validated_data['name'],
            text=validated_data['text'],
            cooking_time=validated_data['cooking_time'],
            author=validated_data['author'],
            image=validated_data['image'])
        for tag in tags:
            recipe.tags.add(tag)
        for ingr in ingredients:
            ingredient = IngredientWithAmount.objects.create(
                amount=ingr['amount'],
                ingredient=get_object_or_404(
                    Ingredient,
                    id=ingr['ingredient']['id'])
            )
            recipe.ingredients.add(ingredient)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        image = validated_data.pop('image', None)
        name = validated_data.pop('name', None)
        text = validated_data.pop('text', None)
        cooking_time = validated_data.pop('cooking_time', None)

        if ingredients:
            instance.ingredients.all().delete()
            for ingr in ingredients:
                ingredient = IngredientWithAmount.objects.create(
                    amount=ingr['amount'],
                    ingredient=get_object_or_404(
                        Ingredient,
                        id=ingr['ingredient']['id'])
                )
                instance.ingredients.add(ingredient)

        if tags:
            instance.tags.clear()
            for tag in tags:
                instance.tags.add(tag)

        if image:
            instance.image = image
        if name:
            instance.name = name
        if text:
            instance.text = text
        if cooking_time:
            instance.cooking_time = cooking_time
        instance.save
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


class RecipePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
