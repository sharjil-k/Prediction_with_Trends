from django.test import TestCase as DJTestCase


from .models import DateTime
import datetime

class BasicModelTestCase(DJTestCase):
    dt = datetime.datetime.now()
    def setUp(self):
         DateTime.objects.create(date = self.dt)

    def test_model_objects_created_properly(self):
       """Does a basic test for the Models function """
       dt_obj = DateTime.objects.get(date=self.dt)
       self.assertEqual(dt_obj.date.strftime("%m/%d/%Y, %H:%M:%S"), self.dt.strftime("%m/%d/%Y, %H:%M:%S"))



