from django.test import TestCase
from order.models import Order, OrderItem


# Create your tests here.
class OrderModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods.
        pass

    def setUp(self):
        # setUp: Run once for every test method to setup clean data.
        pass
