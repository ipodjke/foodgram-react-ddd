from rest_framework import routers

from .apis import IngredientsAPI

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsAPI, basename='ingredients_api_v1')

urlpatterns = router.urls
