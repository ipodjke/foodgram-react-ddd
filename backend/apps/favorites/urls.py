from rest_framework import routers

from .apis import FavoritesAPI

router = routers.DefaultRouter()
router.register(r'recipes_new', FavoritesAPI, basename='favorites_api_new')

urlpatterns = router.urls
