import random

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth import get_user_model

from basket.models import Basket, BasketItem, BasketException
from products.models import Product
from checkout.models import Order


class CreateOrderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # add test products
        number_of_products = 5

        for product_number in range(number_of_products):
            title = f'Doggie Treats {product_number}'
            brand = 'Pawfect'
            category = 'Dog'
            price = round(random.uniform(0, 50), 2)
            description = 'Doggie Treats'
            stock = round(random.uniform(0, 100), 2)
            # image = MagicMock(spec=File, name='FileMock')
            image = SimpleUploadedFile(
                name='image.jpg',
                content=open(settings.BASE_DIR +
                             '/test/image.jpg', 'rb').read(),
                content_type='image/jpeg'
            )
            is_live = True

            product_details = {
                'title': title,
                'brand': brand,
                'category': category,
                'price': price,
                'stock': stock,
                'description': description,
                'image': image,
                'is_live': is_live
            }
            Product.objects.create(**product_details)

    def test_create_order_from_basket(self):
        """Test that the method to create an order works as expected"""

        user = get_user_model().objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='pass1234',
            first_name='Doogan',
            last_name='Doogle',
            address='1234 Test Lane',
            city='Dublin',
            country='Ireland',
            post_code='D01 XE18'
        )

        # create basket
        basket = Basket.objects.create(user=user)
        # get product objects
        product1 = Product.objects.get(title='Doggie Treats 1')
        product2 = Product.objects.get(title='Doggie Treats 2')

        quantity1 = 3
        quantity2 = 5
        quantity = quantity1 + quantity2

        # add products to basket
        BasketItem.objects.create(
            basket=basket, product=product1, quantity=quantity1
        )
        BasketItem.objects.create(
            basket=basket, product=product2, quantity=quantity2
        )

        # create order form basket
        shipping_details = {
            'shipping_name': 'Doogan Doogle',
            'shipping_address': '1234 Test Lane',
            'shipping_city': 'Dublin',
            'shipping_country': 'Ireland',
            'shipping_post_code': 'D01 XE18'
        }

        order = basket.create_order(
            order_details=shipping_details,
            stripe_id='test'
        )

        # perform tests
        self.assertEqual(order.user, user)
        self.assertEqual(order.billing_name,
                         shipping_details.get('shipping_name'))
        self.assertEqual(order.shipping_name,
                         shipping_details.get('shipping_name'))
        self.assertEqual(order.item_count(), quantity)
        # check that the number of order items for each product is equal
        # to quantity
        self.assertEqual(order.orderitem_set.filter(
            product=product1).count(), quantity1)
        self.assertEqual(order.orderitem_set.filter(
            product=product2).count(), quantity2)

    def test_create_order_no_stripe_id(self):
        """No stripe id indicates payment was not made succesfully, raise an
        errror"""

        user = get_user_model().objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='pass1234',
            first_name='Doogan',
            last_name='Doogle',
            address='1234 Test Lane',
            city='Dublin',
            country='Ireland',
            post_code='D01 XE18'
        )

        # create basket
        basket = Basket.objects.create(user=user)
        # get product objects
        product1 = Product.objects.get(title='Doggie Treats 1')
        product2 = Product.objects.get(title='Doggie Treats 2')

        quantity1 = 3
        quantity2 = 5

        # add products to basket
        BasketItem.objects.create(
            basket=basket, product=product1, quantity=quantity1
        )
        BasketItem.objects.create(
            basket=basket, product=product2, quantity=quantity2
        )

        # create order form basket
        shipping_details = {
            'shipping_name': 'Doogan Doogle',
            'shipping_address': '1234 Test Lane',
            'shipping_city': 'Dublin',
            'shipping_country': 'Ireland',
            'shipping_post_code': 'D01 XE18'
        }

        expected_msg = 'Order cannot be created as there was a ' \
            'problem identifying the payment.'
        # create_order called with wrapper to capture exception when raised
        with self.assertRaisesRegex(BasketException, expected_msg):
            basket.create_order(
                order_details=shipping_details
            )

    def test_create_order_empty_basket(self):
        """Test that the method to create an order works as expected"""

        user = get_user_model().objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='pass1234',
            first_name='Doogan',
            last_name='Doogle',
            address='1234 Test Lane',
            city='Dublin',
            country='Ireland',
            post_code='D01 XE18'
        )

        # create basket
        basket = Basket.objects.create(user=user)

        # create order form basket
        shipping_details = {
            'name': 'Doogan Doogle',
            'address': '1234 Test Lane',
            'city': 'Dublin',
            'country': 'Ireland',
            'post_code': 'D01 XE18'
        }

        expected_msg = 'Order cannot be generated as the basket is empty'
        # create_order called with wrapper to capture exception when raised
        with self.assertRaisesRegex(BasketException, expected_msg):
            basket.create_order(
                order_details=shipping_details
            )

    def test_create_order_no_user(self):
        """Test that the method to create an order works as expected"""

        # create basket
        basket = Basket.objects.create(user=None)

        # get product objects
        product1 = Product.objects.get(title='Doggie Treats 1')
        product2 = Product.objects.get(title='Doggie Treats 2')

        quantity1 = 3
        quantity2 = 5

        # add products to basket
        BasketItem.objects.create(
            basket=basket, product=product1, quantity=quantity1
        )
        BasketItem.objects.create(
            basket=basket, product=product2, quantity=quantity2
        )

        # create order form basket
        shipping_details = {}

        expected_msg = 'Order cannot be generated as there is no '\
            'associated user'
        # create_order called with wrapper to capture exception when raised
        with self.assertRaisesRegex(BasketException, expected_msg):
            basket.create_order(
                order_details=shipping_details
            )

    def test_create_order_check_order_status_updates_correctly(self):
        """Test that when stripe_id is passed through the resultant Order
        object status is updated to PAID"""

        user = get_user_model().objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='pass1234',
            first_name='Doogan',
            last_name='Doogle',
            address='1234 Test Lane',
            city='Dublin',
            country='Ireland',
            post_code='D01 XE18'
        )

        # create basket
        basket = Basket.objects.create(user=user)
        # get product objects
        product1 = Product.objects.get(title='Doggie Treats 1')
        product2 = Product.objects.get(title='Doggie Treats 2')

        quantity1 = 3
        quantity2 = 5

        # add products to basket
        BasketItem.objects.create(
            basket=basket, product=product1, quantity=quantity1
        )
        BasketItem.objects.create(
            basket=basket, product=product2, quantity=quantity2
        )

        # create order form basket
        shipping_details = {
            'shipping_name': 'Doogan Doogle',
            'shipping_address': '1234 Test Lane',
            'shipping_city': 'Dublin',
            'shipping_country': 'Ireland',
            'shipping_post_code': 'D01 XE18'
        }

        order = basket.create_order(
            order_details=shipping_details,
            stripe_id='test'
        )

        # perform tests
        self.assertEqual(order.status, Order.PAID)
