from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls


API_TITLE = "Mozio Interview API"
API_DESCRIPTION = "Simple Crud API"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/docs/", include_docs_urls(title=API_TITLE,
                                           description=API_DESCRIPTION)),
    path('api/v1/', include('api.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
