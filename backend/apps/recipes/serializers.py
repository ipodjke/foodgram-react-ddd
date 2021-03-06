import datetime

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

import recipes.services as services
from .models import IngredientsList, Recipe, TagsList


class IngredientsListSerializer(serializers.ModelSerializer):
    ingredient = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = IngredientsList
        fields = ('ingredient', 'amount')

    def get_ingredient(self, obj):
        return services.RecipesService().get_ingredient(pk=obj.ingredient)

    def to_representation(self, instance):
        ingredient = super().to_representation(instance).get('ingredient')
        return {
            'id': ingredient.get('id'),
            'name': ingredient.get('name'),
            'measurement_unit': ingredient.get('measurement_unit'),
            'amount': instance.amount
        }


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    ingredients = IngredientsListSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    publication_date = serializers.DateTimeField(write_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_author(self, obj):
        return services.RecipesService().get_user(request=self.context.get('request'),
                                                  pk=obj.author)

    def get_tags(self, obj):
        return services.RecipesService().get_tags(tags=obj.tags.all())

    def get_is_favorited(self, obj):
        user = self._get_user_from_request(self.context)
        return services.RecipesService().check_is_favorited(
            recipe=obj.id,
            user=user
        )

    def get_is_in_shopping_cart(self, obj):
        user = self._get_user_from_request(self.context)
        return services.RecipesService().check_is_in_shopping_cart(
            recipe=obj.id,
            user=user
        )

    def _get_user_from_request(self, data):
        return data.get('request').user if data.get('request') else None


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    tags = serializers.ListField(
        child=serializers.IntegerField(),
    )
    ingredients = serializers.ListField(
        child=serializers.JSONField(),
    )
    publication_date = serializers.DateTimeField(
        write_only=True,
        default=datetime.datetime.now()
    )

    class Meta:
        model = Recipe
        exclude = ('author',)

    def validate_cooking_time(self, value):
        if int(value) == 0:
            raise serializers.ValidationError(
                '???????????? ???????????? ?????????? ?????????????? = 0'
            )
        return value

    def validate_tags(self, value):
        unique_tags = []
        for tag_id in value:
            if tag_id in unique_tags:
                raise serializers.ValidationError(
                    '???? ?????????? ?????? ???????????????????? ????????'
                )
            unique_tags.append(tag_id)
        return value

    def validate_ingredients(self, value):
        unique_ingredients = []
        for data_ingredient in value:
            ingredient = services.RecipesService().get_ingredient(pk=data_ingredient.get('id'))

            if ingredient in unique_ingredients:
                raise serializers.ValidationError(
                    f'?????????????????????? {ingredient.get("name")}, ???????????????????? ???????????????? ????????'
                    ' ????????????????????.'
                )

            unique_ingredients.append(ingredient)

            if int(data_ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    '???? ?????????? ???? ???????????????????? ???????????????? ('
                    f'{data_ingredient.get("amount")}) ?????? {ingredient.get("name")}'
                )

        return value

    def create(self, validated_data):
        tags = self._get_tags(validated_data)
        ingredients = self._get_ingredients(validated_data)

        recipe = self.Meta.model.objects.create(
            author=self.context.get('request').user.id,
            **validated_data
        )

        self._add_tags_to_recipe(recipe, tags)
        self._add_ingredients_to_recipe(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        tags = self._get_tags(validated_data)
        ingredients = self._get_ingredients(validated_data)

        instance.tags.all().delete()
        self._add_tags_to_recipe(instance, tags)

        instance.ingredients.all().delete()
        self._add_ingredients_to_recipe(instance, ingredients)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance, context=self.context)
        return serializer.data

    def _get_tags(self, validated_data: dict) -> list:
        """
        ???????????????? ????????.
        """
        return validated_data.pop('tags')

    def _get_ingredients(self, validated_data: dict) -> list:
        """
        ???????????????? ??????????????????????.
        """
        return validated_data.pop('ingredients')

    def _add_tags_to_recipe(self, recipe: Recipe, tags: list) -> None:
        """
        ???????????????? ???????????? ?????????? ?? TagsList ?? ?????????????????? ?? ??????????????.
        """
        for tag in tags:
            TagsList.objects.create(
                recipe=recipe,
                tag=tag,
            )

    def _add_ingredients_to_recipe(self,
                                   recipe: Recipe,
                                   ingredients: list) -> None:
        """
        ???????????????? ?????????????????????? ?? IngredientList ??????????????.
        """
        for ingredient in ingredients:
            IngredientsList.objects.create(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
