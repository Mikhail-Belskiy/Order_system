from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Retail Order API",
      default_version='v1',
   ),
   public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('swagger/', schema_view.with_ui('swagger')),
]
urlpatterns += [
    path('', include('shop.urls_api')),
]