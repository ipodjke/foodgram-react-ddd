from rest_framework import routers

from .apis import IngredientsAPI

router = routers.DefaultRouter()
router.register(r'ingredients_new', IngredientsAPI, basename='ingredients_api_new')

urlpatterns = router.urls
