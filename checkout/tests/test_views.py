import random

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..views import process_order
from basket.models import Basket, BasketItem
from products.models import Product


class ViewCheckoutTest(TestCase):
    """Test access to checkout"""

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

        # create empty basket
        self.basket = Basket.objects.create(user=self.user)

        # set product variables
        self.product1 = Product.objects.get(title='Doggie Treats 1')
        self.product2 = Product.objects.get(title='Doggie Treats 2')

    def test_view_not_accessible_when_user_logged_out(self):
        """Test that an anonymous user cannot access view, redirected to
        login"""
        response = self.client.get(self.reverse_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/accounts/login/')

    def test_view_not_accessible_when_basket_does_not_exist(self):
        """Check that when user is logged in but has no items in basket,
        they are redirected to the basket view"""
        self.client.force_login(user=self.user)
        response = self.client.get(self.reverse_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/basket/')

    def test_view_not_accessible_when_basket_is_empty(self):
        """User basket object exists, but there are not items in the basket.
        User should be redirected to basket"""

        # create request
        request = self.factory.get(self.reverse_url)

        # add basket and user objects to request (required by view)
        request.user = self.user
        # add empty basket object to request (no items, count = 0)
        request.basket = self.basket

        response = process_order(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/basket/')

    def test_view_when_basket_has_items(self):
        """Test that checkout view works correctly when a user is logged in and
        has a basket with items."""

        # set product variables
        quantity1 = 6
        quantity2 = 3

        # add items to basket
        BasketItem.objects.create(
            basket=self.basket, product=self.product1, quantity=quantity1)
        BasketItem.objects.create(
            basket=self.basket, product=self.product2, quantity=quantity2)

        # create request
        request = self.factory.get(self.reverse_url)
        # add basket and user objects to request (required by view)
        request.basket = self.basket
        request.user = self.user

        response = process_order(request)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """Check the template used is the intended one"""

        # login
        self.client.force_login(user=self.user)

        # add products via http request
        url = reverse('add_to_basket', kwargs={'product_id': self.product1.id})
        # load page (execute add to basket)
        self.client.get(url)

        # go to checkout
        response = self.client.get(self.reverse_url)

        # run tests
        self.assertTemplateUsed(
            response, template_name='checkout/order_processing.html')

    def test_checkout_submission_with_invalid_stripe_token(self):
        """Create a POST submission for the checkout form with all necessary
        fields, including an invalid stripe-token"""

        # get user object
        user = self.user

        # login
        self.client.force_login(user=user)

        # add products via http request
        url = reverse('add_to_basket', kwargs={'product_id': self.product1.id})
        # load page (execute add to basket)
        self.client.get(url)

        # create form data
        name = f'{user.first_name} {user.last_name}'
        form_details = {
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
            # stripe-token is invalid, expect an error
            'stripe-token': 'test123'
        }

        # submit form
        response = self.client.post(
            self.reverse_url, data=form_details, follow=True)

        # run tests
        self.assertTemplateUsed(
            response, template_name='checkout/order_processing.html')
        self.assertContains(response,
                            'There was a problem processing your order, '
                            'please try again.')
