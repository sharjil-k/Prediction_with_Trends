from django.core.management import BaseCommand
import boto3

from django.db import transaction


from personalcapital.financial_tasks import FetchFinancialData
import json
from datetime import datetime

from dask.dataframe import read_csv, read_parquet, to_csv, to_parquet
from ...models import DateTime, FinancialData
import argparse
parser = argparse.ArgumentParser(description='data set')

FileName = 'data/display.txt'
BucketName = 'displayproject'

class Command(BaseCommand):
    help = "Load review facts"
    S3 = boto3.client('s3')


    def add_arguments(self, parser):
        parser.add_argument("-t", "--test", action="store_true")

    def handle(self, *args, **options):
        test = options['test']

        obj_financial = FinancialData.objects.latest('date')
        print(obj_financial.total_assets)

        with open(FileName, 'w') as f:
           # f.write("Assets: $" + str(obj_financial.total_assets))
            f.write(' Cash Accounts             : ' + '${:,.0f}\n'.format(obj_financial.cash_accounts))
            f.write(' Investment Accounts       : ' + '${:,.0f}\n'.format(obj_financial.stock_accounts))
            f.write(' Retirement Accounts       : ' + '${:,.0f}\n'.format(obj_financial.retirement_accounts))
            f.write(' Other (Home & Car) : ' + '${:,.0f}\n'.format(obj_financial.other_assets))
            f.write(' TOTAL ASSETS              : ' + '${:,.0f}\n'.format(obj_financial.total_assets))
            f.write("\n")
            # Liabilities
            f.write(' Credit Cards        : ' + '${:,.0f}\n'.format(obj_financial.credit_card_accounts))
            f.write(' Loan Accounts       : ' + '${:,.0f}\n'.format(obj_financial.loan_accounts))
            f.write(' Mortgage            : ' + '${:,.0f}\n'.format(obj_financial.mortgage_accounts))
            f.write(' TOTAL LIABILITIES   : ' + '${:,.0f}\n'.format(obj_financial.total_liabilities))
            f.write("\n")
            f.write(' NET WORTH           : ' + '${:,.0f}'.format(obj_financial.networth))


            ## SOME MESSAGE FOR THE USER BASED ON ANALYTICS
            sorted = FinancialData.objects.all().order_by('-date')
            stock_accounts_now = sorted[0].stock_accounts
            stock_accounts_yesterday = sorted[1].stock_accounts
            if (abs(stock_accounts_yesterday - stock_accounts_now))/stock_accounts_now > 0.03 :
               f.write('\n\nYour stock accounts changed by more than 3% today!!' )

        self.S3.upload_file(FileName, BucketName, FileName, ExtraArgs={'ACL': 'public-read'})




