from django.contrib import admin

# Register your models here.
from .models import DateTime, ModelingData

admin.site.register(DateTime)
admin.site.register(ModelingData)