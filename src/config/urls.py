from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="Aca Drive API",
        default_version='v1',
        description="This is for all client of Aca Drive",
        terms_of_service="https://www.AcaDrive.com/policies/terms/",
        contact=openapi.Contact(email="acadrive.ca@gmail.com"),
        license=openapi.License(name="ACADrive License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

docpatterns = []

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('config.auth.Users.urls')),
    path('pricing/', include('config.apps.ClientHub.urls.pricing_urls')),
    path('plans/', include('config.apps.ClientHub.urls.plans_urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json', schema_view.without_ui(cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_title = "Aca Drive"
admin.site.index_title = "Aca Drive"
admin.site.site_header = "Aca Drive"

handler404 = 'config.utils.views.error_404'
handler500 = 'config.utils.views.error_500'
