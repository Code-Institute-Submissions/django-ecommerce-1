import random
import uuid

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage

from ..views import view_basket, add_to_basket
from ..models import Basket, BasketItem
from products.models import Product


class ViewBasketTest(TestCase):
    """Test the GET view for ViewBasket"""

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
        self.manual_url = '/basket/'
        self.reverse_url = reverse('basket')
        self.factory = RequestFactory()

        # create basket
        self.basket = Basket.objects.create(user=None)
        # set product variables
        self.product1 = Product.objects.get(title='Doggie Treats 1')
        self.product2 = Product.objects.get(title='Doggie Treats 2')

    def test_view_url_exists(self):
        """Check that the hardcoded page exists"""
        response = self.client.get(self.manual_url)
        self.assertEqual(response.status_code, 200)

    def test_view_reverse_url(self):
        """Check that the named view page exists"""
        response = self.client.get(self.reverse_url)
        self.assertEqual(response.status_code, 200)

    def test_basket_without_items(self):
        """check output when basket is empty"""
        response = self.client.get(self.reverse_url)
        self.assertContains(response, 'You do not have any items in your '
                            'basket')

    def test_basket_with_items(self):
        """Add items to basket and check that they are displayed on basket
        view"""
        quantity = 3
        expected_total = self.product1.price * quantity

        # add items to basket
        BasketItem.objects.create(
            basket=self.basket, product=self.product1, quantity=quantity)

        # create request
        request = self.factory.get(self.reverse_url)
        # add basket object to request, required by view
        request.basket = self.basket

        response = view_basket(request)

        # perform tests
        self.assertContains(response, 'Shopping Basket')
        self.assertContains(response, self.product1.title)
        self.assertContains(response, self.product1.price)
        self.assertContains(response, expected_total)

    def test_basket_icon_badge_reflects_basket_quantity(self):
        """Test that the basket badge in the navbar always reflects the
        quantity of items in the basket"""

        quantity1 = 2
        quantity2 = 5

        # add items to basket
        BasketItem.objects.create(
            basket=self.basket, product=self.product1, quantity=quantity1)
        BasketItem.objects.create(
            basket=self.basket, product=self.product2, quantity=quantity2)

        total_quantity = quantity1 + quantity2

        # create request
        request = self.factory.get(self.reverse_url)
        # add basket object to request, required by view
        request.basket = self.basket
        response = view_basket(request)

        # perform tests
        self.assertContains(response, '<span class="badge badge-pill '
                            f'badge-warning cart-badge">{total_quantity}'
                            '</span>')

    def test_update_basket(self):
        """Update quantity of items in basket"""
        quantity = 3

        BasketItem.objects.create(
            basket=self.basket, product=self.product1, quantity=quantity)

        # create request
        request = self.factory.get(self.reverse_url)
        # add basket object to request, required by view
        request.basket = self.basket
        response = view_basket(request)

        # perform intial test
        self.assertContains(response,
                            f'There are {quantity} item(s) in your basket.')

        # update quantity and re-run test
        updated_quantity = 4
        BasketItem.objects.all().update(quantity=updated_quantity)
        response = view_basket(request)

        # perform intial test
        self.assertContains(response,
                            f'There are {updated_quantity} item(s) '
                            'in your basket.')

    def test_item_subtotal(self):
        """Check item subtotals output the correct amount"""
        # set product variables
        quantity1 = 6
        quantity2 = 3

        # add items to basket
        item1 = BasketItem.objects.create(
            basket=self.basket, product=self.product1, quantity=quantity1)
        item2 = BasketItem.objects.create(
            basket=self.basket, product=self.product2, quantity=quantity2)

        # create request
        request = self.factory.get(self.reverse_url)
        # add basket object to request, required by view
        request.basket = self.basket
        response = view_basket(request)

        subtotal1 = self.product1.price * quantity1
        subtotal2 = self.product2.price * quantity2

        self.assertEqual(item1.subtotal(), subtotal1)
        self.assertEqual(item2.subtotal(), subtotal2)

        # check basket for subtotal values
        self.assertContains(response, subtotal1)
        self.assertContains(response, subtotal2)

    def test_basket_total(self):
        """Check basket total outputs the correct amount"""
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
        # add basket object to request, required by view
        request.basket = self.basket
        response = view_basket(request)

        subtotal1 = self.product1.price * quantity1
        subtotal2 = self.product2.price * quantity2

        total = subtotal1 + subtotal2

        # run tests
        self.assertEqual(self.basket.total(), total)
        self.assertContains(response, total)

    def test_basket_is_emptied_upon_logout(self):
        """Test that basket is cleared when a user logs out of account"""
        email = 'test@user.com'
        password = 'pass1234'
        user = get_user_model().objects.create_user(
            username=email,
            email=email,
            password=password)
        user_basket = Basket.objects.create(user=user)

        quantity1 = 1
        quantity2 = 2

        # add items to basket
        BasketItem.objects.create(
            basket=user_basket, product=self.product1, quantity=quantity1)
        BasketItem.objects.create(
            basket=user_basket, product=self.product2, quantity=quantity2)

        # log in to user account (returns boolean)
        logged_in = self.client.login(email=email, password=password)

        # make sure the user logged in successfully
        self.assertTrue(logged_in)

        # goto basket and check that the items are there
        response = self.client.get(self.reverse_url)
        self.assertContains(response, self.product1.title)
        self.assertContains(response, self.product2.title)

        # log out of account
        self.client.logout()

        # load basket view and check contents
        response = self.client.get(self.reverse_url)
        # make sure user is no longer logged in
        self.assertTrue(response.context['user'].is_authenticated is False)
        # now check basket contents
        self.assertNotContains(response, self.product1.title)
        self.assertNotContains(response, self.product2.title)
        self.assertContains(
            response, 'You do not have any items in your basket.')


class AddToBasketTest(TestCase):
    """Test how products are added to the basket using add_to_basket view"""

    @classmethod
    def setUpTestData(cls):
        # add test products
        number_of_products = 10

        for product_number in range(number_of_products):
            title = f'Doggie Treats {product_number}'
            brand = 'Pawfect'
            category = 'Dog'
            price = round(random.uniform(0, 50), 2)
            description = 'Doggie Treats'
            stock = round(random.uniform(0, 100), 2)
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
        """ """
        # create products
        self.basket_url = reverse('basket')
        self.factory = RequestFactory()
        # create basket
        self.basket = Basket.objects.create(user=None)

    def test_add_valid_product(self):
        """Check that adding product with a valid product uuid, results in
        product being added to the basket view"""
        product = Product.objects.get(title='Doggie Treats 9')
        url = reverse('add_to_basket', kwargs={'product_id': product.id})

        # create request
        request = self.factory.get(url)
        # add middleware to request
        request.session = {}
        request.session['basket_id'] = self.basket.id
        request._messages = FallbackStorage(request)
        # add basket object to request, required by view
        request.basket = self.basket
        # process view
        response = add_to_basket(request, product.id)
        # check that response returns redirect to basket
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/basket/')
        # given add_to_basket results in a redirect, which can not be handled
        # by RequestFactory, basket view is manually called and tests run
        # against this view
        basket_response = view_basket(request)
        # test that product appears on basket view
        self.assertContains(basket_response, 'Shopping Basket')
        self.assertContains(basket_response, product.title)

    def test_add_invalid_product(self):
        """Check that adding product with an invalid product uuid results in
        an error being raised"""
        # create a random uuid
        product_id = uuid.uuid4()

        url = reverse('add_to_basket', kwargs={'product_id': product_id})
        # create request
        response = self.client.get(url)

        # product id is invalid so view should return 404 not found
        self.assertEqual(response.status_code, 404)

    def test_add_product_with_invalid_uuid(self):
        """Test that if user provides an invalid uuid, an error is raised"""
        # create a random uuid
        product_id = 'abcd2123'

        url = '/basket/add/' + product_id + '/'
        # create request
        response = self.client.get(url)

        # product id is invalid so view should return 404 not found
        self.assertEqual(response.status_code, 404)

    def test_add_item_exceed_maximum_quantity(self):
        """Ensure that a basket item cannot exceed maximum permitted amount"""
        # store product details
        product = Product.objects.get(title='Doggie Treats 9')
        quantity = 4

        # add item to basket
        BasketItem.objects.create(
            basket=self.basket, product=product, quantity=quantity)

        # now that basket has item at maximum permitted quantity, try to add
        # product (which increases quantity by +1) - this should NOT result in
        # a quantity increase
        url = reverse('add_to_basket', kwargs={'product_id': product.id})
        # create request
        request = self.factory.get(url)
        # add middleware to request
        request.session = {}
        request.session['basket_id'] = self.basket.id
        request._messages = FallbackStorage(request)
        # add basket object to request, required by view
        request.basket = self.basket

        # before running the add_to_basket view, check quantity in basket
        basket_response = view_basket(request)
        self.assertContains(basket_response, f'There are {quantity} item(s)'
                            ' in your basket')

        # run the view
        # item is already in basket, therefore, quantity will be increased
        # BUT only if it does not exceed max quantity
        add_to_basket(request, product.id)  # results in +1 quantity
        # load basket and check quantity
        basket_response = view_basket(request)
        self.assertContains(basket_response, f'There are {quantity + 1} '
                            'item(s) in your basket')

        # run view again - this time quantity should not change
        # because max quantity has been reached
        add_to_basket(request, product.id)  # results in +1 quantity
        # load basket and check quantity
        basket_response = view_basket(request)
        self.assertContains(basket_response, f'There are {quantity + 1} '
                            'item(s) in your basket')


class GetBasketTest(TestCase):
    """Test view for merging basket, if anonymous user logs in to
    account/restoring user's basket"""
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
        self.basket_url = reverse('basket')
        self.email = 'test@test.com'
        self.password = 'test1234'

        self.user = get_user_model().objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password)
        # create a basket for the user
        self.basket = Basket.objects.create(user=self.user)
        # get products for adding to user basket
        self.product1 = Product.objects.get(title='Doggie Treats 1')
        self.product2 = Product.objects.get(title='Doggie Treats 2')
        self.quantity1 = 4
        self.quantity2 = 1

        # add items to the user's basket
        self.item1 = BasketItem.objects.create(
            basket=self.basket, product=self.product1, quantity=self.quantity1)
        self.item2 = BasketItem.objects.create(
            basket=self.basket, product=self.product2, quantity=self.quantity2)

    def test_restore_users_basket(self):
        """Test that user's stored basket is restored when they log in"""
        # user is not logged in - anonymous user
        # check contents of basket, prior to log-in (expect to be empty)
        response = self.client.get(self.basket_url)
        self.assertContains(response, 'You do not have any items in '
                            'your basket')

        # log in to user account and check basket contents match those above
        self.client.force_login(self.user)

        # setup test variables
        total = self.quantity1 + self.quantity2

        # goto basket and check contents
        response = self.client.get(self.basket_url)
        # check each product appears in user's basket
        self.assertContains(response, self.product1.title)
        self.assertContains(response, self.product2.title)
        # check model quantities against test quantities
        self.assertContains(response, f'There are {total} '
                            'item(s) in your basket.')
        self.assertEqual(total, self.basket.count())

    def test_merge_users_basket(self):
        """Test that contents of anonymous basket are merged into user's stored
        basket upon account login (uses user_logged_in signal) """

        # get product object
        new_product = Product.objects.get(title='Doggie Treats 3')

        # user is currently anonymous - add items to anonymous user's basket
        # via add_to_basket view, this will redirect user to basket view
        response = self.client.get(
            reverse('add_to_basket', kwargs={'product_id': new_product.id}),
            follow=True)
        self.assertContains(response, 'Shopping Basket')
        self.assertContains(response, new_product.title)
        # by default add_to_basket view sets quantity to 1
        self.assertContains(response, 'There are 1 item(s) in your basket.')

        # log in to user account - expect basket above to merge with the basket
        # created in setUp() method
        login_details = {
            'login': self.email,
            'password': self.password
        }

        login_response = self.client.post(
            '/accounts/login/', login_details, follow=True)
        # make sure the user logged in successfully
        self.assertTrue(login_response.context['user'].is_authenticated)

        # goto basket and check contents
        response = self.client.get(self.basket_url)

        # setup test variables
        new_product_quantity = 1
        total = new_product_quantity + self.quantity1 + self.quantity2

        # run tests
        # product added before login
        self.assertContains(response, new_product.title)
        # products that already existed in the users saved basket
        self.assertContains(response, self.product2.title)
        self.assertContains(response, self.product2.title)
        # check model quantities against test quantities
        self.assertContains(response, f'There are {total} '
                            'item(s) in your basket.')
        self.assertEqual(total, self.basket.count())
