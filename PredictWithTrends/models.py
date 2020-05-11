from django.db import models

class DateTime(models.Model):
    date = models.DateTimeField('time')

class ModelingData(models.Model):
    date = models.OneToOneField(DateTime, on_delete=models.CASCADE, primary_key=True)
    y = models.FloatField(default=0)  # The time series data that we are trying to forecast
    trend1=models.FloatField(default=0)  # trend Data to use to improve the model
    trend2=models.FloatField(default=0)  # trend data to use to improve the model
    trend3=models.FloatField(default=0)  # trend data to use to improve the model
    trend4=models.FloatField(default=0)  # trend data to use to improve the model