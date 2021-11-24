from rest_framework import routers

from .apis import ShoppingCartRestAPI

router = routers.DefaultRouter()
router.register(r'recipes', ShoppingCartRestAPI, basename='shopping_cart_api_v1')

urlpatterns = router.urls
