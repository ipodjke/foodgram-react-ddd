from rest_framework import routers

from .apis import RecipesAPI

router = routers.DefaultRouter()
router.register(r'recipes', RecipesAPI, basename='recipes_api_v1')

urlpatterns = router.urls
