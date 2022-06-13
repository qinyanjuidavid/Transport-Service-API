from rest_framework.routers import SimpleRouter
from django.views.generic import TemplateView
from django.urls import path

from transport.views import ProviderAPIView

app_name = "api"
routes = SimpleRouter()

routes.register('provider/', ProviderAPIView,
                basename="provider")
# routes.register('servicearea/', ProviderAPIView,
#                 basename="servicearea")

urlpatterns = [
    *routes.urls,
]
