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


