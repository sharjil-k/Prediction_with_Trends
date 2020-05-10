## Some code came from open source Capital One API: https://github.com/haochi/personalcapital

from personalcapital import PersonalCapital, RequireTwoFactorException, TwoFactorVerificationModeEnum
from luigi import ExternalTask, Parameter, Task, format, LocalTarget, DateParameter, BoolParameter, build


import getpass
import json
import logging
import os
import ftplib





class PewCapital(PersonalCapital):
    """
    Extends PersonalCapital to save and load session
    So that it doesn't require 2-factor auth every time
    """

    def __init__(self):
        PersonalCapital.__init__(self)
        self.__session_file = 'session.json'

    def load_session(self):
        try:
            with open(self.__session_file) as data_file:
                cookies = {}
                try:
                    cookies = json.load(data_file)
                except ValueError as err:
                    logging.error(err)
                self.set_session(cookies)
        except IOError as err:
            logging.error(err)

    def save_session(self):
        with open(self.__session_file, 'w') as data_file:
            data_file.write(json.dumps(self.get_session()))


def get_email():
    email = os.getenv('PERSONAL_CAP_USERNAME')
    if not email:
        print(
            'You can set the environment variables for PERSONAL_CAP_USERNAME and PERSONAL_CAP_PASSWORD so the prompts don\'t come up every time')
        return input('Enter personal capital user-email:')
    return email


def get_password():
    password = os.getenv('PERSONAL_CAP_PASSWORD')

    if not password:
        return getpass.getpass('Enter personal capital password:')
    return password


def uploadFileFTP(sourceFilePath, destinationDirectory, server, username, password):
    myFTP = ftplib.FTP(server, username, password)
    #   if destinationDirectory in [name for name, data in list(remote.mlsd())]:
    #       print ("Destination Directory does not exist. Creating it first")
    #       myFTP.mkd(destinationDirectory)
    # Changing Working Directory
    myFTP.cwd(destinationDirectory)
    if os.path.isfile(sourceFilePath):
        fh = open(sourceFilePath, 'rb')
        myFTP.storbinary('STOR Personal_Capital_data_Pi.txt', fh)
        fh.close()
    else:
        print("Source File does not exist")


## LUIGI TASKS TO CONNECT AND RETRIEVE THE DATA

class ConnectAuthenticate(Task):
    pc = PewCapital()

    def requires(self):
        return []

    def output(self):
        return LocalTarget("financial_data.txt")
        accounts_response = self.pc.fetch('/newaccount/getAccounts')
        print(accounts_response.json())
        return accounts_response

    def run(self):
        email, password = get_email(), get_password()
        self.pc.load_session()

        try:
            self.pc.login(email, password)
        except RequireTwoFactorException:
            self.pc.two_factor_challenge(TwoFactorVerificationModeEnum.SMS)
            self.pc.two_factor_authenticate(TwoFactorVerificationModeEnum.SMS, input('code: '))
            self.pc.authenticate_password(password)


class GetFinancialData(Task):
    pc = PewCapital()
    def requires(self):
        return []

    def output(self):
        return LocalTarget("data/financial_data.json")

    def run(self):
        email, password = get_email(), get_password()
        self.pc.load_session()

        try:
            self.pc.login(email, password)
        except RequireTwoFactorException:
            self.pc.two_factor_challenge(TwoFactorVerificationModeEnum.SMS)
            self.pc.two_factor_authenticate(TwoFactorVerificationModeEnum.SMS, input('code: '))
            self.pc.authenticate_password(password)

        accounts_data = self.pc.fetch('/newaccount/getAccounts').json()['spData']

        with self.output().open('w') as outfile:
            json.dump(accounts_data, outfile)


def FetchFinancialData():
    build([
        GetFinancialData(),
        ],
        local_scheduler=True)