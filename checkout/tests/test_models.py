import random

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Order, OrderItem
from products.models import Product


class CheckoutModelTests(TestCase):
    """Test model functionality"""

    @classmethod
    def setUpTestData(cls):
        # add test products
        number_of_products = 3

        for product_number in range(number_of_products):
            title = f'Doggie Treats {product_number}'
            brand = 'Pawfect'
            category = 'Dog'
            # stripe only accepts payment amounts > 0.50
            price = round(random.uniform(1, 50), 2)
            description = 'Doggie Treats'
            stock = int(random.uniform(0, 100))
            is_live = True

            product_details = {
                'title': title,
                'brand': brand,
                'category': category,
                'price': price,
                'stock': stock,
                'description': description,
                'image': SimpleUploadedFile(
                    name='image.jpg',
                    content=open(settings.BASE_DIR +
                                 '/test/image.jpg', 'rb').read(),
                    content_type='image/jpeg'
                ),
                'is_live': is_live
            }
            Product.objects.create(**product_details)

    def setUp(self):
        self.reverse_url = reverse('checkout')
        self.factory = RequestFactory()

        self.username = 'test@test.com'
        self.password = 'test1234'

        self.user = get_user_model().objects.create_user(
            username=self.username,
            email=self.username,
            password=self.password,
            first_name='Test',
            last_name='McTest',
            address='123 Four Five',
            post_code='D01 82EP',
            city='Dublin',
            country='Ireland')

        # set product variables
        self.product1 = Product.objects.get(title='Doggie Treats 1')
        self.product2 = Product.objects.get(title='Doggie Treats 2')

        user = self.user

        # create order
        name = f'{user.first_name} {user.last_name}'
        order_details = {
            'user': user,
            'status': Order.NEW,
            'billing_name': name,
            'billing_address': user.address,
            'billing_city': user.city,
            'billing_country': user.country,
            'billing_post_code': user.address,
            'shipping_name': name,
            'shipping_address': user.address,
            'shipping_city': user.city,
            'shipping_country': user.country,
            'shipping_post_code': user.address,
            'stripe_id': 'test123'
        }

        self.order = Order.objects.create(**order_details)

        # add items to order
        self.item1 = OrderItem.objects.create(
            order=self.order,
            status=OrderItem.IN_PROGRESS,
            product=self.product1,
            price=self.product1.price,
        )
        self.item2 = OrderItem.objects.create(
            order=self.order,
            status=OrderItem.PICKED,
            product=self.product1,
            price=self.product1.price,
        )
        self.item3 = OrderItem.objects.create(
            order=self.order,
            status=OrderItem.NEW,
            product=self.product2,
            price=self.product2.price,
        )

    def test_str_method(self):
        """ Test the output of __str__ """
        order = self.order

        order_txt = str(order)

        str_txt = f'Date: {order.order_date} - User: {order.user.username} ' \
            f'- ID: {order.id} - Items: {order.item_count()}'

        self.assertEqual(order_txt, str_txt)

    def test_method_item_count(self):
        """ Test the output of item_count() method """
        # 3 order items created in setup
        item_count = 3

        self.assertEqual(item_count, self.order.item_count())

    def test_method_status_progress(self):
        """ Test the output of status_progress() method which results a
        numeric value for populating a status bar."""

        # status_progress() outputs a percentage. The first status choice
        # should return 0%, the final status should return 100%.
        expected_status = 0
        self.assertEqual(expected_status, self.order.status_progress())

    def test_method_total(self):
        """ Test the output of total() method """
        # 3 order items created in setup
        order_total = self.item1.price + self.item2.price + self.item3.price

        self.assertEqual(order_total, self.order.total())
