from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import ModelingData
from .serializers import ModelingDataSerializer

class ModelingDataView(ModelViewSet):
    queryset = ModelingData.objects.all()
    serializer_class= ModelingDataSerializer

