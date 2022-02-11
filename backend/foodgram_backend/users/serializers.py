from django.contrib.auth import get_user_model
from djoser.conf import settings
from rest_framework import serializers

from food.models import Recipe

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        if self.context['request'].user.followers.filter(
            follower=obj
        ).exists():
            return True
        return False

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
        ) + ('is_subscribed',)
        read_only_fields = (settings.LOGIN_FIELD,)


class RecipePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
        ) + ('is_subscribed', 'recipes')

    def get_recipes(self, obj):
        serialized_data = RecipePartSerializer(
            data=obj.recipes.all(),
            many=True)
        return serialized_data.data
