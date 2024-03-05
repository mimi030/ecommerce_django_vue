from django.test import TestCase
"""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework import status
import json
from product.models import Category, Product  # Import your models
from order.serializers import OrderSerializer

class CheckoutViewTest(TestCase):
    def setUp(self):
        # Create a user and obtain an authentication token
        self.user = User.objects.create_user(username='john123', password='testpassword')
        self.token = Token.objects.create(user=self.user).key

        # Create test data (adjust based on your actual data model)
        self.category = Category.objects.create(name='Chicken', slug='chicken')
        self.product = Product.objects.create(
            category=self.category,
            name='Chicken Thighs',
            slug='chicken_thighs',
            description='yummy and juicy chicken thighs',
            price=10.0
        )

        # Set up the order data
        self.order_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'city': 'City',
            'state': 'State',
            'zip_code': '12345',
            'phone': '555-555-5555',
            'stripe_token': 'stripe_token_here',
            'items': [
                {
                    'price': str(self.product.price),
                    'product': {'id': self.product.id, 'name': self.product.name, 'price': str(self.product.price)},
                    'quantity': 2,
                }
            ],
            'paid_amout': str(20.0),
        }

    def test_checkout_view_authenticated(self):
        # Set up the request
        url = reverse('checkout')  # Assuming you have a name for the checkout URL
        request_data = json.dumps(self.order_data)
        request = self.client.post(
            url,
            data=request_data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )

        # Make the request to the view
        response = checkout(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # You may want to add more assertions based on the expected behavior of your view

    def test_checkout_view_unauthenticated(self):
        # Set up the request
        url = reverse('checkout')  # Assuming you have a name for the checkout URL
        request_data = json.dumps(self.order_data)
        request = self.client.post(
            url,
            data=request_data,
            content_type='application/json'
        )

        # Make the request to the view
        response = checkout(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # You may want to add more assertions based on the expected behavior of your view
"""
