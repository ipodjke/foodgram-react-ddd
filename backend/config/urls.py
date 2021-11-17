from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from ingredients.views import IngredientsViewSet
from recipes.views import RecipeViewSet
from tags.views import TagsViewSet
from users.views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/v2/', include('tags.urls')),
    path('api/v2/', include('ingredients.urls')),
    path('api/v2/', include('subscriptions.urls')),
    path('api/v2/', include('users.urls')),
    path('api/v2/', include('favorites.urls')),
    path('api/v2/', include('shoping_cart.urls')),
    path('api/v2/', include('recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
