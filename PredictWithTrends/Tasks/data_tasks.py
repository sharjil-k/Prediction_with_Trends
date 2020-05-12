import os
import datetime as dt
from django.core.management import BaseCommand
import fbprophet
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from luigi import  Task, LocalTarget, build
import matplotlib.pyplot as plt
import pandas as pd
import quandl
from ..models import DateTime, ModelingData

TEST_PERCENTAGE = 0.95

class GetData(Task):
    def requires(self):
        return []

    def output(self):
        return LocalTarget("data/getdata_SUCCESS")

    def run(self):
        try:
            quandl.ApiConfig.api_key = os.environ['QUANDL_API_KEY']
            data = quandl.get('WIKI/TSLA')
        except RequireTwoFactorException:
            print("Could not find the data in the remote server")

        df = data[['Close','Volume']].copy()
        wf = df.resample('W').mean()
        wf.head()
        wf.reset_index(inplace=True)
        wf.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
        print(wf)

        #Plot data
        plt.figure(figsize=(8, 8))
        plt.plot(wf['ds'], wf['y'])
        plt.title('TRAINING DATA')
        plt.show(block=False)

        df_records = wf.to_dict('records')

        time_objs = [DateTime(date=record['ds']) for record in df_records]

        DateTime.objects.all().delete()
        DateTime.objects.bulk_create(time_objs)

        data_objs = [ModelingData(date=DateTime.objects.get(date=record['ds']), y= record['y'], trend1 = record['Volume']) for record in df_records]
        ModelingData.objects.all().delete()
        ModelingData.objects.bulk_create(data_objs)

        with self.output().open('w') as f:
            f.write("Data Fetched Successfully")

class AddTrends(Task):
    def requires(self):
        return [GetData()]

    def output(self):
        return LocalTarget("data/trends_SUCCESS")

    def run(self):
        df = pd.DataFrame(list(ModelingData.objects.all().values()))
        dates = pd.DataFrame(list(DateTime.objects.all().values()))
        df['ds'] = dates['date'].values

        # Find the trends from internet using API.
        # Not working right now so feed some trends data from a file

        # Capture the valid trends data
        trends = pd.read_csv("multiTimeline.csv")
        trends.dtypes
        df['trend2'] = 0
        for index, row in trends.iterrows():
            year = row['Month'].split('-')[0].lstrip("0")
            month = row['Month'].split('-')[1].lstrip("0")
            value = row['Trend']

            for indexD, rowD in df.iterrows():
                if (str(rowD['ds'].year) == str(year)) & (str(rowD['ds'].month) == str(month)):
                    df['trend2'].iloc[indexD] = value

        # Store everything back to the database
        df_records = df.to_dict('records')
        data_objs = [ModelingData(date=DateTime.objects.get(date=record['ds']), y= record['y'], trend1 = record['trend1'], trend2= record['trend2']) for record in df_records]
        ModelingData.objects.all().delete()
        ModelingData.objects.bulk_create(data_objs)


        with self.output().open('w') as f:
            f.write("Adding Trends Successfully")

class ModelPredict(Task):
    def requires(self):
        return [AddTrends()]

    def run(self):
        df = pd.DataFrame(list(ModelingData.objects.all().values()))
        dates = pd.DataFrame(list(DateTime.objects.all().values()))
        df['ds'] = dates['date'].values

        data_train, data_test = np.split(df, [int(TEST_PERCENTAGE * len(df))])


        # Train Model
        m = fbprophet.Prophet(changepoint_prior_scale=0.15)
        m_r = fbprophet.Prophet(changepoint_prior_scale=0.15)
        m_r.add_regressor('trend2')
        m.fit(data_train)
        m_r.fit(data_train)

        # Create future data set
        future = m.make_future_dataframe(periods=len(data_test), freq='1W')
        future.shape
        future['trend2'] = df['trend2']

        # The Forecast
        forecast = m.predict(future)
        forecast_r = m_r.predict(future)

        fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 8))
        fig.suptitle('TRAINING DATA AND MODELFORECAST WITH CONFIDENCE INTERVAL', y=1.05, fontsize=20)
        m.plot(forecast, ax=ax1, xlabel='Date', ylabel='Stock Price (in $)')
        ax1.set_title('WITHOUT REGRESSOR')
        m.plot(forecast_r, ax=ax2, xlabel='Date', ylabel='Stock Price (in $)')
        ax2.set_title('WITH REGRESSOR')
        fig.tight_layout(pad=3.0)

        plt.show()



def RunGetData():
    build([GetData()],local_scheduler=True)

def RunModelPredict():
    build([ModelPredict()],local_scheduler=True)

RunGetData()