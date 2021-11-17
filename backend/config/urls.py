from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

api_v1_patterns = [
    path('', include('tags.urls')),
    path('', include('ingredients.urls')),
    path('', include('subscriptions.urls')),
    path('', include('users.urls')),
    path('', include('favorites.urls')),
    path('', include('shopping_cart.urls')),
    path('', include('recipes.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include(api_v1_patterns)),
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
