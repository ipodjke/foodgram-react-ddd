from rest_framework import routers

from .apis import UsersRestAPI

router = routers.DefaultRouter()
router.register(r'users', UsersRestAPI, basename='users_api_v1')

urlpatterns = router.urls
