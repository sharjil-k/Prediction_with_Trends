from django.contrib import admin

# Register your models here.
from .models import DateTime, FinancialData

admin.site.register(DateTime)
admin.site.register(FinancialData)
