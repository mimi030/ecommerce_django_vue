# from django.test import TestCase
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
# from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from order.models import Order, OrderItem
from product.models import Product, Category
from order.serializers import (
    MyOrderSerializer,
    MyOrderItemSerializer,
    OrderItemSerializer,
    OrderSerializer,
)
import json
from unittest.mock import patch


class CreateAndLoginAccountTest(APITestCase):
    """ Test module for POST Djoser user registration and login api  """
    def setUp(self):
        # Create test data
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        """
        self.test_user = {
            'username': 'john123',
            'password': 'testpassword',
        }
        self.invalid_test_user = {
            'username': '12345',
            'password': 'test!!!',
        }
        self.invalid_login_user = {
            'username': 'invalid_user',
            'password': 'invalid_password',
        }
        self.invalid_login_user_missing_pw = {
            'username': '12345',
            'password': '',
        }

    def test_valid_create_account(self):
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        """
        # Making a POST request for user creation
        response = self.client.post('/api/v1/users/', data=self.test_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.test_user['username'])

    def test_invalid_create_account(self):
        # Making a POST request for user creation
        response = self.client.post('/api/v1/users/', data=self.invalid_test_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_login(self):
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/token/login', data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        """
        # Creating a user using the defined test data
        self.client.post('/api/v1/users/', data=self.test_user)

        # Making a POST request for user login
        response = self.client.post('/api/v1/token/login/', data=self.test_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        # Creating a user using the defined test data
        self.client.post('/api/v1/users/', data=self.test_user)

        # Making a POST request for user login
        response = self.client.post('/api/v1/token/login/', data=self.invalid_login_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_get_user_list(self):
        pass


class CreateMyOrderTest(APITestCase):
    def setUp(self):
        # Create test data
        self.test_user = {
            'username': 'john123',
            'password': 'testpassword',
        }
        Category.objects.create(
            name='Chicken', slug='chicken'
        )
        Product.objects.create(
            category=Category.objects.get(name='Chicken'), name='Chicken Thighs', slug='chicken_thighs', description='yummy and juicy chicken thighs', price=10.0
        )
        self.product = Product.objects.get(name='Chicken Thighs')
        self.order_item_data = {
            'price': str(self.product.price),
            'product': {
                'id': self.product.id,
                'name': self.product.name,
                'price': str(self.product.price),
            },
            'quantity': 2,
        }
        self.order_data = {
            'id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'city': 'City',
            'state': 'State',
            'zip_code': '12345',
            'phone': '555-555-5555',
            'stripe_token': 'stripe_token_here',
            'items': [self.order_item_data],
            'paid_amout': str(20.0),
        }

    def test_valid_create_order_item(self):
        serializer = MyOrderItemSerializer(data=self.order_item_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data

        # self.assertEqual(serialized_data['price'], 13.5)
        self.assertEqual(serialized_data['product']['name'], 'Chicken Thighs')
        self.assertEqual(serialized_data['quantity'], 2)

    def test_invalid_create_order_item(self):
        pass

    def test_valid_create_order(self):
        pass

    def test_invalid_create_order(self):
        pass


class CheckoutMyOrderTest(APITestCase):
    def setUp(self):
        # Create test data
        self.test_user = {
            'username': 'john123',
            'password': 'testpassword',
        }
        Category.objects.create(
            name='Chicken', slug='chicken'
        )
        Product.objects.create(
            category=Category.objects.get(name='Chicken'), name='Chicken Thighs', slug='chicken_thighs', description='yummy and juicy chicken thighs', price=10.0
        )
        self.product = Product.objects.get(name='Chicken Thighs')
        self.order_item_data = {
            'price': str(self.product.price),
            'product': self.product.id,
            'quantity': 2,
        }
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
            'items': [self.order_item_data],
            'paid_amount': 20.0,
        }

    def authenticate_user(self):
        # Create a user using Djoser's registration endpoint
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Obtain an authentication token using Djoser's login endpoint
        login_data = {
            'username': self.test_user['username'],
            'password': self.test_user['password']
        }
        response = self.client.post(
            '/api/v1/token/login/',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Return the token
        return response.data.get('auth_token')

    @patch('stripe.Charge.create')
    def test_valid_checkout(self, mock_stripe_charge_create):
        # Authenticate the user and obtain the token
        auth_token = self.authenticate_user()

        # Use the obtained token to authenticate the user in the checkout request
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')

        # Mock the Stripe API call
        mock_stripe_charge_create.return_value = {'id': 'fake_charge_id', 'status': 'succeeded'}

        serializer = OrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid(), f"Serializer errors: {serializer.errors}")
        # Print if serializer is valid
        print(f"{self._testMethodName} serializer is_valid:")
        print(serializer.is_valid())
        serialized_data = serializer.data

        # Make the checkout request
        response = self.client.post(
            '/api/v1/checkout/',
            data=json.dumps(serialized_data),
            content_type='application/json'
        )
        # Print the response content for debugging
        print(f"{self._testMethodName} response content:")
        print(response.data)
        # Print serialized data
        print(f"{self._testMethodName} serialized data:")
        print(json.dumps(serialized_data, indent=2))
        # Print serialized data items
        print(f"{self._testMethodName} serialized data items:")
        print(serialized_data['items'])
        # Assert the expected status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve the order from the database
        order_id = response.data['id']
        order = Order.objects.get(id=order_id)

        # Print order details for debugging
        print(f"{self._testMethodName} Order Details:")
        print(f"Order ID: {order.id}")
        print(f"Paid Amount: {order.paid_amount}")
        print(f"User: {order.user}")
        print(f"Items: {order.items.all()}")

        # Make a request to the OrderList view
        response = self.client.get('/api/v1/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the order is present in the order list
        self.assertEqual(len(response.data), 1)
        # Assert paid amount in the orders list
        self.assertEqual(response.data[0]['paid_amount'], format(order.paid_amount, '.2f'))

        # Check the calculated paid amount directly
        # calculated_paid_amount = sum(item['quantity'] * Product.objects.get(id=item['product']).price for item in serialized_data['items'])

    def test_invalid_checkout(self):
        # Authenticate the user and obtain the token
        auth_token = self.authenticate_user()

        # Use the obtained token to authenticate the user in the checkout request
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')

        # incomplete data
        invalid_order_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'city': 'City',
            'state': 'State',
            'zip_code': '12345',
            'phone': '555-555-5555',
        }

        # Make the invalid checkout request
        response = self.client.post(
            '/api/v1/checkout/',
            data=json.dumps(invalid_order_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_get_orders_list(self):
        """ Test for GET orders list """
        # Authenticate the user and obtain the token
        auth_token = self.authenticate_user()

        # Use the obtained token to authenticate the user in the checkout request
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')

        # Make a request to the OrderList view with authentication
        response = self.client.get('/api/v1/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_get_orders_list(self):
        # Not authenticate the user and making the request without a valid token
        self.client.credentials()

        # Make the request to the OrderList view without authentiation
        response = self.client.get('/api/v1/orders/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


"""
class MyOrderSerializerTest(APITestCase):
    def setup(self):
        # Create test data
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.order_item_data = {
            'price': 10.0,
            'product': {
                'id': self.product.id,
                'name': 'Test Product',
                'price': 10.0
            },
            'quantity': 2,
        }
        self.order_data = {
            #'id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'city': 'City',
            'state': 'State',
            'zip_code': '12345',
            'phone': '555-555-5555',
            'stripe_token': 'stripe_token_here',
            'items': [self.order_item_data],
            'paid_amout': 20.0,
        }
        # Create test user account
        self.user = User.objects.create(
            username="testaccount00",
            email="testaccount00@email.com",
            password="password"
        )

    def test_my_order_item_serializer(self):
        serializer = MyOrderItemSerializer(data=self.order_item_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data

        self.assertEqual(serialized_data['price'], 10.0)
        self.assertEqual(serialized_data['product']['name'], 'Test Product')
        self.assertEqual(serialized_data['quantity'], 2)

    def test_my_order_serializer(self):
        serializer = MyOrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data

        self.assertEqual(serialized_data['first_name'], 'John')
        self.assertEqual(serialized_data['email'], 'john@example.com')

        self.assertIsInstance(serialized_data['items'], list)
        self.assertEqual(len(serialized_data['item']), 1)
        self.assertEqual(serialized_data['items'][0]['price'], 10.0)
        self.assertEqual(serialized_data['items'][0]['quantity'], 2)

    def test_order_item_serializer(self):
        serializer = OrderItemSerializer(data=self.order_item_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data

        self.assertEqual(serialized_data['price'], 10.0)
        self.assertEqual(serialized_data['quantity'], 2)

    def test_order_serializer(self):
        serializer = OrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data

        self.assertEqual(serialized_data['first_name'], 'John')
        self.assertEqual(serialized_data['email'], 'john@example.com')

        self.assertIsInstance(serialized_data['items'], list)
        self.assertEqual(len(serialized_data['items']), 1)
        self.assertEqual(serialized_data['items'][0]['price'], 10.0)
        self.assertEqual(serialized_data['items'][0]['quantity'], 2)

    def test_order_create_method(self):
        serializer = MyOrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid())

        order = serializer.save()

        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.email, 'john@example.com')

        self.assertEqual(order.items.count(), 1)
        item = order.items.first()
        self.assertEqual(item.price, 10.0)
        self.assertEqual(item.quantity, 2)
"""
