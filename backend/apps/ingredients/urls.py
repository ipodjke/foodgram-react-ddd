from rest_framework import routers

from .apis import IngredientsRestAPI

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsRestAPI, basename='ingredients_api_v1')

urlpatterns = router.urls
