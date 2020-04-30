import random

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from checkout.models import Order, OrderItem
from products.models import Product


class ViewOrderHistoryTests(TestCase):
    """Test access and content of order history page"""

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
        self.reverse_url = reverse('order_history')

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

    def test_public_cannot_access_page(self):
        """ Test that page redirects to login page when anonymous """
        response = self.client.get(self.reverse_url)

        self.assertRedirects(response,
                             '/accounts/login/?next=/orders/history/')

        self.assertTemplateNotUsed(
            response, template_name='orders/order_history.html')

    def test_page_accessible_when_logged_in(self):
        """The page should be accessible when the user is logged in"""
        # login to account
        self.client.force_login(user=self.user)

        response = self.client.get(self.reverse_url)

        # run tests
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name='orders/order_history.html')
