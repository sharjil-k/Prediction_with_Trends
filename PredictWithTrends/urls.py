from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from .views import ModelingDataView

router = DefaultRouter()

# Register some endpoints via "router.register(...)"

router.register(r'modelingdata', ModelingDataView)


schema_view = get_schema_view(title="Prediction with Trends API")

urlpatterns = [
    path("api/", include(router.urls)),
]