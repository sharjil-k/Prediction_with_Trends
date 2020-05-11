from rest_framework import serializers

from .models import DateTime, ModelingData

class DateTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTime
        fields = '__all__'

class ModelingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelingData
        fields = '__all__'
