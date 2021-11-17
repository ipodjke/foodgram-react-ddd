from rest_framework import routers

from .apis import UsersAPI

router = routers.DefaultRouter()
router.register(r'users_new', UsersAPI, basename='users_api_new')

urlpatterns = router.urls
