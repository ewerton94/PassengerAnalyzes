from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from core.routes import router as core_routes
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_swagger_view(title='API Passageiros')

urlpatterns = [
    path('', schema_view),
    path('admin/', admin.site.urls),
    path('core/', include(core_routes.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)