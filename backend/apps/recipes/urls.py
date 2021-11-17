from rest_framework import routers

from .apis import RecipesAPI

router = routers.DefaultRouter()
router.register(r'recipes_new', RecipesAPI, basename='recipes_api_new')

urlpatterns = router.urls
