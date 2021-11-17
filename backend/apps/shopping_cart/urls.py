from rest_framework import routers

from .apis import ShoppingCartAPI

router = routers.DefaultRouter()
router.register(r'recipes', ShoppingCartAPI, basename='shopping_cart_api_v1')

urlpatterns = router.urls
