import datetime as dt
from django.core.management import BaseCommand
import fbprophet
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import boto3

from django.db import transaction


from personalcapital.financial_tasks import FetchFinancialData
import json
from datetime import datetime

from dask.dataframe import read_csv, read_parquet, to_csv, to_parquet
from ...models import ModelingData, DateTime
import argparse
parser = argparse.ArgumentParser(description='data set')

TEST_PERCENTAGE = 0.95

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("-t", "--test", action="store_true")

    def handle(self, *args, **options):
        df = pd.DataFrame(list(ModelingData.objects.all().values()))
        dates = pd.DataFrame(list(DateTime.objects.all().values()))
        df['ds'] = dates['date'].values

        print(df)

        #dates_list = [dt.datetime.strptime(DateTime.objects.get(id=row['date_id']).date,"%Y-%m-%d") for row in df.iterrows()]
        #print(dates_list)
        #df['ds']=dates_list
        print(df)
       # df.reset_index(inplace=True)
        #df.rename(columns={'date_id': 'ds'}, inplace=True)
        #df['ds'] = DateTime.objects.get(id=df['date_id'])

        data_train, data_test = np.split(df, [int(TEST_PERCENTAGE * len(df))])
        print(data_train)
        # Plot The training set
        plt.figure(figsize=(20, 10))
        plt.plot(data_train['ds'], data_train['y'])
        plt.title('TRAINING DATA')
        plt.show(block=False)

        # Train Model
        m = fbprophet.Prophet(changepoint_prior_scale=0.15)
        m_r = fbprophet.Prophet(changepoint_prior_scale=0.15)
        m_r.add_regressor('trend1')
        m.fit(data_train)
        m_r.fit(data_train)

        # Create future data set
        future = m.make_future_dataframe(periods=len(data_test), freq='1W')
        future.shape
        future['trend1'] = df['trend1']

        # The Forecast
        forecast = m.predict(future)
        forecast_r = m_r.predict(future)

        # Plot the Modeling metrics
        f = m_r.plot_components(forecast)

        # Plot the forecast
        #% matplotlib qt
        # %matplotlib inline
        fig, (ax1, ax2) = plt.subplots(2, figsize=(20, 20))
        fig.suptitle('TRAINING DATA AND MODELFORECAST WITH CONFIDENCE INTERVAL', y=1.05, fontsize=20)
        m.plot(forecast, ax=ax1, xlabel='Date', ylabel='Stock Price (in $)')
        ax1.set_title('WITHOUT REGRESSOR')
        m.plot(forecast_r, ax=ax2, xlabel='Date', ylabel='Stock Price (in $)')
        ax2.set_title('WITH REGRESSOR')
        fig.tight_layout(pad=3.0)
        # m.plot(forecast, ax = ax1, xlabel = 'Date', ylabel = 'Stock Price (in $)')
        # m.plot(forecast, ax = ax2, xlabel = 'Date', ylabel = 'Stock Price (in $)')
        # plt.plot(data_test['y'])
        # metric_df[['y','yhat']].plot()
        # plt.title('Stock Price of Tesla');
        plt.show()



