from rest_framework import routers

from .apis import FavoritesAPI

router = routers.DefaultRouter()
router.register(r'recipes', FavoritesAPI, basename='favorites_api_v1')

urlpatterns = router.urls
