from django.db import models

class DateTime(models.Model):
    date = models.DateTimeField('time')

class FinancialData(models.Model):
    date = models.OneToOneField(DateTime, on_delete=models.CASCADE, primary_key=True)
    fake_data = models.BooleanField(default=False)  # To distinguish between test data and real data
    # Assets
    cash_accounts = models.IntegerField(default=0)  # Integer field; number of reviews on that date
    stock_accounts = models.FloatField(default=0)  # Integer, sum of review.stars for all reviews on that date
    retirement_accounts = models.FloatField(default=0)
    other_assets = models.FloatField(default=0)
    total_assets = models.FloatField(default=0)
    # Liabilities
    credit_card_accounts = models.FloatField(default=0)
    loan_accounts = models.FloatField(default=0)
    mortgage_accounts = models.FloatField(default=0)
    credit_cards = models.FloatField(default=0)
    credit_cards = models.FloatField(default=0)
    total_liabilities =  models.FloatField(default=0)
    #networth
    networth = models.FloatField(default=0)