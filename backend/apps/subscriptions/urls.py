from rest_framework import routers

from .apis import SubscriptionsRestAPI

router = routers.DefaultRouter()
router.register(r'users', SubscriptionsRestAPI, basename='subsciptions_api_v1')

urlpatterns = router.urls
