from rest_framework import routers

from .apis import ShopingCartAPI

router = routers.DefaultRouter()
router.register(r'recipes_new', ShopingCartAPI, basename='shoping_cart_api_new')

urlpatterns = router.urls
