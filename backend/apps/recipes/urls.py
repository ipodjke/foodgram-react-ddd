from rest_framework import routers

from .apis import RecipesRestAPI

router = routers.DefaultRouter()
router.register(r'recipes', RecipesRestAPI, basename='recipes_api_v1')

urlpatterns = router.urls
