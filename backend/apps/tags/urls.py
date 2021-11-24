from rest_framework import routers

from .apis import TagsRestAPI

router = routers.DefaultRouter()
router.register(r'tags', TagsRestAPI, basename='tags_api_v1')

urlpatterns = router.urls
