from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from .views import FinancialDataView

router = DefaultRouter()

# Register some endpoints via "router.register(...)"

router.register(r'financial', FinancialDataView)


schema_view = get_schema_view(title="Yelp Review API")

urlpatterns = [
    path("api/", include(router.urls)),
]