import argparse
from django.core.management import BaseCommand

from ...Tasks.data_tasks import RunGetData


parser = argparse.ArgumentParser(description='data set')


class Command(BaseCommand):
    help = "Load review facts"

    def add_arguments(self, parser):
        parser.add_argument("-t", "--test", action="store_true")

    def handle(self, *args, **options):
        RunGetData()
        # test = options['test']
        #
        # # Run the Luigi tasks to retrieve Financial Data.
        # if test :
        #     file_path = 'financial_data.json'
        # else :
        #     FetchFinancialData()
        #     file_path = 'data/financial_data.json'
        #
        # with open(file_path) as json_file:
        #     accounts = json.load(json_file)

        #     # GET THE VALUE OF 401k ACCOUNTS (retirement accounts)
        # balance_401k = 0
        # for item in accounts["accounts"]:
        #        if item["firmName"] == 'Fidelity NetBenefits (401k) (US)':
        #             balance_401k = balance_401k + item["currentBalance"]
        #
        #
        # # Assets
        # cash_accounts = accounts['cashAccountsTotal']
        # investment_accounts = accounts['investmentAccountsTotal'] - balance_401k
        # retirement_accounts = balance_401k
        # other_assets = accounts['otherAssetAccountsTotal']
        # Total_Assets = accounts['assets']
        #
        # # Liabilities
        # credit_card_accounts = accounts['creditCardAccountsTotal']
        # loan_accounts = accounts['loanAccountsTotal']
        # mortgage_accounts = accounts['mortgageAccountsTotal']
        # Total_Liabilities = accounts['liabilities']
        #
        # NetWorth = accounts['networth']
        #
        # #Assets
        # print(' Cash Accounts             : ' + '${:,.0f}'.format(cash_accounts))
        # print(' Investment Accounts       : ' + '${:,.0f}'.format(investment_accounts))
        # print(' Retirement Accounts       : ' + '${:,.0f}'.format(retirement_accounts))
        # print(' Other Assets (Home & Car) : ' + '${:,.0f}'.format(other_assets))
        # print(' TOTAL ASSETS              : ' + '${:,.0f}'.format(Total_Assets))
        # print("")
        # # Liabilities
        # print(' Credit Cards        : ' + '${:,.0f}'.format(credit_card_accounts))
        # print(' Loan Accounts       : ' + '${:,.0f}'.format(loan_accounts))
        # print(' Mortgage            : ' + '${:,.0f}'.format(mortgage_accounts))
        # print(' TOTAL LIABILITIES   : ' + '${:,.0f}'.format(Total_Liabilities))
        # print("")
        # print(' NET WORTH           : ' + '${:,.0f}'.format(NetWorth))
        #
        # timestamp = datetime.now()
        #
        #
        # time_obj = DateTime(date = timestamp)
        # time_obj.save()
        # data_obj = FinancialData (
        #     date=DateTime.objects.get(date=timestamp),
        #     fake_data= test,  # To distinguish between test data and real data
        #         # Assets
        #     cash_accounts = cash_accounts,  # Integer field; number of reviews on that date
        #     stock_accounts = investment_accounts,  # Integer, sum of review.stars for all reviews on that date
        #     retirement_accounts = retirement_accounts,
        #     other_assets = other_assets,
        #     total_assets = Total_Assets,
        #
        #     # Liabilities
        #     credit_card_accounts = credit_card_accounts,
        #     loan_accounts = loan_accounts,
        #     mortgage_accounts = mortgage_accounts,
        #     total_liabilities = Total_Liabilities,
        #
        #     #Net Worth
        #     networth = NetWorth,
        # )
        #
        # data_obj.save()



