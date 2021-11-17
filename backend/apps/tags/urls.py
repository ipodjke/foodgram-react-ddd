from rest_framework import routers

from .apis import TagsAPI

router = routers.DefaultRouter()
router.register(r'tags_new', TagsAPI, basename='tags_api_new')

urlpatterns = router.urls
