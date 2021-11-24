from rest_framework import routers

from .apis import FavoritesRestAPI

router = routers.DefaultRouter()
router.register(r'recipes', FavoritesRestAPI, basename='favorites_api_v1')

urlpatterns = router.urls
