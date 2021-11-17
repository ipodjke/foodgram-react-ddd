from rest_framework import routers

from .apis import SubscriptionsAPI

router = routers.DefaultRouter()
router.register(r'users_new', SubscriptionsAPI, basename='subsciptions_api_new')

urlpatterns = router.urls
