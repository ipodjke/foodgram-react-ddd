from rest_framework import routers

from .apis import SubscriptionsAPI

router = routers.DefaultRouter()
router.register(r'users', SubscriptionsAPI, basename='subsciptions_api_v1')

urlpatterns = router.urls
