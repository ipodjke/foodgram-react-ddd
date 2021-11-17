from rest_framework import routers

from .apis import TagsAPI

router = routers.DefaultRouter()
router.register(r'tags', TagsAPI, basename='tags_api_v1')

urlpatterns = router.urls
