from rest_framework import routers

from .apis import UsersAPI

router = routers.DefaultRouter()
router.register(r'users', UsersAPI, basename='users_api_v1')

urlpatterns = router.urls
