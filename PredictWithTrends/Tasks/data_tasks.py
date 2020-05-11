import os
from luigi import  Task, LocalTarget, build
import pandas as pd
import quandl
from ..models import DateTime, ModelingData

class GetData(Task):
    def requires(self):
        return []

    def output(self):
        return LocalTarget("data/data.csv")

    def run(self):
        try:
            #quandl.ApiConfig.api_key = os.environ['QUANDL_API_KEY']
            quandl.ApiConfig.api_key = '29hyErz2TzC5oZFLCJkw'
            print("Here")
            data = quandl.get('WIKI/TSLA')
        except RequireTwoFactorException:
            print("Could not find the data in the remote server")

        df = data[['Close','Volume']].copy()
        wf = df.resample('W').mean()
        wf.head()
        wf.reset_index(inplace=True)
        wf.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
        print(wf)

        df_records = wf.to_dict('records')

        time_objs = [DateTime(date=record['ds']) for record in df_records]

        DateTime.objects.all().delete()
        DateTime.objects.bulk_create(time_objs)

        data_objs = [ModelingData(date=DateTime.objects.get(date=record['ds']), y= record['y'], trend1 = record['Volume']) for record in df_records]
        ModelingData.objects.all().delete()
        ModelingData.objects.bulk_create(data_objs)
       # data_obj = FinancialData (
       #     date=DateTime.objects.get(date=timestamp),
       #     fake_data= test,  # To distinguish between test data and real data
       #         # Assets
       #     cash_accounts = cash_accounts,  # Integer field; number of reviews on that date
       #     stock_accounts = investment_accounts,  # Integer, sum of review.stars for all reviews on that date
       #     retirement_accounts = retirement_accounts,
       #     other_assets = other_assets,
       #     total_assets = Total_Assets,

       #    # Liabilities
       #     credit_card_accounts = credit_card_accounts,
       #     loan_accounts = loan_accounts,
       #     mortgage_accounts = mortgage_accounts,
       #     total_liabilities = Total_Liabilities,

            #Net Worth
        #    networth = NetWorth,
       # )

      #  data_obj.save()

        #with self.output().open('w') as outfile:
        #    self.output.write(data)


def RunGetData():
    build([
        GetData(),
        ],
        local_scheduler=True)

RunGetData()