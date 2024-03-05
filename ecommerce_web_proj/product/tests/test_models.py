from django.test import TestCase
from django.urls import reverse
import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product.models import Category, Product
from product.serializers import ProductSerializer, CategorySerializer


class CreateProductTest(TestCase):
    """ Test module for Product model """

    def setUp(self):
        Category.objects.create(
            name='Beef', slug='beef'
        )
        Product.objects.create(
            category=Category.objects.get(name='Beef'), name='Wangyu', slug='wangyu', description='yummy and juicy beef', price='10'
        )

    def test_valid_create_product(self):
        product_wangyu = Product.objects.get(name='Wangyu')
        self.assertEqual(
            product_wangyu.category.name, "Beef"
        )

    def test_invalid_create_product(self):
        product_wangyu = Product.objects.get(name='Wangyu')
        self.assertEqual(
            product_wangyu.category.name, "Beef"
        )


client = APIClient()


class GetAllProductTest(APITestCase):
    """ Test module for Creating Product model by client and GET all products """

    def setUp(self):
        Category.objects.create(
            name='Chicken', slug='chicken'
        )
        Category.objects.create(
            name='Beef', slug='beef'
        )
        Product.objects.create(
            category=Category.objects.get(name='Chicken'), name='Chicken Thighs', slug='chicken_thighs', description='yummy and juicy chicken thighs', price='13.5'
        )
        Product.objects.create(
            category=Category.objects.get(name='Chicken'), name='Chicken Wings', slug='chicken_wing', description='yummy and juicy chicken wings', price='18.5'
        )
        Product.objects.create(
            category=Category.objects.get(name='Beef'), name='Beef Rib Eyes', slug='beef_rib_eyes', description='yummy and juicy beef rib eyes', price='17'
        )

    def test_get_all_products(self):
        # get API response
        response = client.get(reverse('get_post_products'))
        # get data from db
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleProductTest(APITestCase):
    """ Test module for GET single product API """

    def setUp(self):
        Category.objects.create(
            name='Chicken', slug='chicken'
        )
        Category.objects.create(
            name='Beef', slug='beef'
        )
        self.chicken_thighs = Product.objects.create(
            category=Category.objects.get(name='Chicken'), name='Chicken Thighs', slug='chicken_thighs', description='yummy and juicy chicken thighs', price=13.5
        )
        self.chicken_wings = Product.objects.create(
            category=Category.objects.get(name='Chicken'), name='Chicken Wings', slug='chicken_wing', description='yummy and juicy chicken wings', price=18.5
        )
        self.beef_rib_eyes = Product.objects.create(
            category=Category.objects.get(name='Beef'), name='Beef Rib Eyes', slug='beef_rib_eyes', description='yummy and juicy beef rib eyes', price=17
        )

    def test_get_valid_single_product(self):
        response = client.get(
            reverse('get_delete_update_product', kwargs={'category_slug': self.chicken_wings.category.slug, 'product_slug': self.chicken_wings.slug})
        )
        product = Product.objects.get(category=self.chicken_wings.category, name=self.chicken_wings.name)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Access the primary key of the instance
        product_pk = product.pk
        # Dynamically retrieve the pk from the reverse function
        reverse_product_pk = response.data['id']
        # Ensure that the dynamically retrieved pk matches the actual pk
        self.assertEqual(reverse_product_pk, product_pk)
        print(f"The primary key of {product} is {product_pk}")

    def test_get_invalid_single_product(self):
        response = client.get(
            reverse('get_delete_update_product', kwargs={'category_slug': 'fish', 'product_slug': 'salmon_fillet'})
        )

        # Print the status code for debugging
        print(f"{self._testMethodName} - Response Status Code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
