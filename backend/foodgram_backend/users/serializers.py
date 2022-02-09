from django.contrib.auth import get_user_model
from djoser.compat import get_user_email, get_user_email_field_name
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

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)


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
        if serialized_data.is_valid():
            print(serialized_data.data)
        return serialized_data.data
