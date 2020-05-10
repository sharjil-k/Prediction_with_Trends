from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import FinancialData
from .serializers import FinancialDataSerializer

class FinancialDataView(ModelViewSet):
    queryset = FinancialData.objects.all()
    serializer_class= FinancialDataSerializer

