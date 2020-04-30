import random

from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from ..models import Product, Review


class ProductListViewTest(TestCase):
    """Product list view tests"""

    @classmethod
    def setUpTestData(cls):
        """Creates data one time prior to executing tests"""
        # create products
        number_of_products = 30

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
                # simulate the content required for imagefield
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
        self.manual_url = '/products/'
        self.reverse_url = reverse('product_list')

        # create user
        self.user = get_user_model().objects.create_user(
            username='test_user@email.com',
            email='test_user@email.com',
            password='pass123')

    def test_view_url_exists(self):
        """Check that the hardcoded page exists"""
        response = self.client.get(self.manual_url)
        self.assertEqual(response.status_code, 200)

    def test_view_reverse_url(self):
        """Check that the named view page exists"""
        response = self.client.get(self.reverse_url)
        self.assertEqual(response.status_code, 200)

    def test_product_is_live_false_detail_view_not_displayed(self):
        """Product should not display on list detail view when is_live=False"""
        # change all products so they are not visible
        Product.objects.all().update(is_live=False)

        response = self.client.get(self.reverse_url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertContains(response, 'Products')
        self.assertNotContains(response, '€')
        self.assertNotContains(response, 'Add to basket')

    def test_view_with_no_products(self):
        """List view should show text when no products exist in db"""
        # delete all products
        Product.objects.all().delete()

        response = self.client.get(self.reverse_url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] is False)
        self.assertContains(
            response, 'There are currently no products to display')
        self.assertContains(response, 'Products')
        self.assertNotContains(response, 'Add to basket')

    def test_view_template(self):
        """Make sure the correct template is used to render page"""
        response = self.client.get(self.reverse_url)
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_view_panigation(self):
        """Make sure only the specified number of products per paged"""
        response = self.client.get(self.reverse_url)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['product_list']), 8)

    def test_view_does_not_contain_admin_not_logged_in(self):
        """When not logged in, user should not see admin options"""
        response = self.client.get(self.reverse_url)
        self.assertNotContains(response, 'admin')
        self.assertNotContains(response, 'New Product')
        self.assertNotContains(response, 'Update')
        self.assertNotContains(response, 'Delete')

    def test_view_does_not_contain_admin_logged_in_no_permissions(self):
        """User does not have permissions, should not see admin options"""
        self.client.force_login(self.user)
        response = self.client.get(self.reverse_url)
        self.assertNotContains(response, 'admin')
        self.assertNotContains(response, 'New Product')
        self.assertNotContains(response, 'Update')
        self.assertNotContains(response, 'Delete')

    def test_view_shows_admin_options(self):
        """When logged in with admin permissions, page should show admin
        options """
        permission1 = Permission.objects.get(name='Can add product')
        permission2 = Permission.objects.get(name='Can change product')
        permission3 = Permission.objects.get(name='Can delete product')
        # add permissions to user and login
        self.user.user_permissions.add(permission1, permission2, permission3)
        self.client.force_login(self.user)

        response = self.client.get(self.reverse_url)
        self.assertContains(response, 'Admin')
        self.assertContains(response, 'New Product')
        self.assertContains(response, 'Update')
        self.assertContains(response, 'Delete')


class ProductDetailView(TestCase):
    """Product detail view tests"""

    def setUp(self):
        title = f'Doggie Treats 1'
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
            # simulate the content required for imagefield
            'image': SimpleUploadedFile(
                name='image.jpg',
                content=open(settings.BASE_DIR +
                             '/test/image.jpg', 'rb').read(),
                content_type='image/jpeg'
            ),
            'is_live': is_live
        }
        self.product = Product.objects.create(**product_details)

        self.manual_url = '/products/' + str(self.product.id) + '/'
        self.reverse_url = reverse('product_detail', kwargs={
                                   'pk': self.product.id})

        # create user
        self.user = get_user_model().objects.create_user(
            username='test_user@email.com',
            email='test_user@email.com',
            password='pass123')

    def test_view_url_exists(self):
        """Check that the hardcoded page exists"""
        response = self.client.get(self.manual_url)
        self.assertEqual(response.status_code, 200)

    def test_view_reverse_url(self):
        """Check that the named view page exists"""
        response = self.client.get(self.reverse_url)
        self.assertEqual(response.status_code, 200)

    def test_view_invalid_product_id(self):
        response = self.client.get('/products/asdasd/')
        # page should return 404, not found
        self.assertEqual(response.status_code, 404)

    def test_product_is_live_false_detail_view_not_displayed(self):
        """Product should not display on the detail view when is_live=False"""
        # update product field
        Product.objects.filter(id=self.product.id).update(is_live=False)

        response = self.client.get(self.reverse_url)
        self.assertEqual(response.status_code, 404)

    def test_view_template(self):
        """Make sure the correct template is used to render page"""
        response = self.client.get(self.reverse_url)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_view_displays_product_details(self):
        """Check that product details are shown as part of detail view"""
        response = self.client.get(self.reverse_url)
        self.assertContains(response, self.product.title)
        self.assertContains(response, self.product.brand)
        self.assertContains(response, self.product.price)
        self.assertContains(response, self.product.description)

    def test_view_context_fields_exist(self):
        """Check that context fields are passed through the response object"""
        response = self.client.get(self.reverse_url)
        self.assertTrue('product' in response.context)
        self.assertTrue('product_rating' in response.context)
        self.assertTrue('form' in response.context)

    def test_view_product_rating(self):
        """Test that the product rating display is the average of those
        submitted for product"""
        number_of_reviews = 23
        rating_score = 0
        for review_number in range(number_of_reviews):
            # randomly generate rating
            product = self.product
            rating = int(random.uniform(1, 5))
            review = 'Product rating'
            user = self.user

            Review.objects.create(
                product=product, rating=rating, review=review, user=user)

            rating_score += rating

        response = self.client.get(self.reverse_url)

        # create product rating by taking the average and compare to db output
        product_rating = int(rating_score / number_of_reviews)
        self.assertTrue('product_rating' in response.context)
        self.assertEqual(int(response.context['product_rating']),
                         product_rating)

    def test_view_does_not_contain_admin_not_logged_in(self):
        """When not logged in, user should not see admin options"""
        response = self.client.get(self.reverse_url)
        self.assertNotContains(response, 'admin')
        self.assertNotContains(response, 'Update')
        self.assertNotContains(response, 'Delete')

    def test_view_does_not_contain_admin_logged_in_no_permissions(self):
        """User does not have permissions, should not see admin options"""
        self.client.force_login(self.user)
        response = self.client.get(self.reverse_url)
        self.assertNotContains(response, 'admin')
        self.assertNotContains(response, 'Update')
        self.assertNotContains(response, 'Delete')

    def test_view_shows_admin_options(self):
        """When logged in with admin permissions, page should show admin
        options """
        permission1 = Permission.objects.get(name='Can add product')
        permission2 = Permission.objects.get(name='Can change product')
        permission3 = Permission.objects.get(name='Can delete product')
        # add permissions to user and login
        self.user.user_permissions.add(permission1, permission2, permission3)
        self.client.force_login(self.user)

        response = self.client.get(self.reverse_url)
        self.assertContains(response, 'Admin')
        self.assertContains(response, 'Update')
        self.assertContains(response, 'Delete')


class ProductReviewTest(TestCase):
    """ tests """
    @classmethod
    def setUpTestData(cls):
        """Creates data one time prior to executing tests"""
        # create products
        number_of_products = 1

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
                # simulate the content required for imagefield
                'image': SimpleUploadedFile(
                    name='image.jpg',
                    content=open(settings.BASE_DIR +
                                 '/test/image.jpg', 'rb').read(),
                    content_type='image/jpeg'
                ),
                'is_live': is_live
            }
            product = Product.objects.create(**product_details)

        # create dummy users with a review for each
        number_of_users = 3
        dummy_user = {}

        for user_number in range(number_of_users):
            dummy_user[user_number] = get_user_model().objects.create_user(
                username=f'test_user{user_number}@email.com',
                email=f'test_user{user_number}@email.com',
                password='pass123')

            # create review for user and product
            rating = int(random.uniform(1, 5))
            review = 'Product rating'

            Review.objects.create(
                product=product,
                rating=rating,
                review=review,
                user=dummy_user[user_number])

    def setUp(self):
        self.product = Product.objects.get()
        # store variables to be accessed throughout rest of testing class
        self.reverse_url = reverse('product_detail', kwargs={
            'pk': self.product.id})

    def test_view_displays_all_comments(self):
        """Check that all product reviews are displayed on detail view"""
        # get all reviews for product
        reviews = Review.objects.filter(product=self.product)
        response = self.client.get(self.reverse_url)
        # check that number of reviews in db is same as in view
        self.assertTrue(reviews.count() ==
                        response.context['product'].reviews.count())
        # check contents of one review appears on product view
        review = reviews.first()
        self.assertContains(response, review.user)
        self.assertContains(response, review.review)

    def test_review_form_does_not_display_not_logged_in(self):
        """When user is not logged in, do not display review form"""
        response = self.client.get(self.reverse_url)
        # review form is passed through in context as form
        self.assertTrue('form' in response.context)
        # form will only be displayed if 'display_form' is true
        self.assertTrue('display_form' not in response.context)
        self.assertNotContains(response, 'Add a product review')

    def test_review_form_displays_no_previous_review(self):
        """Form should display if user is logged in and has not previously
        reviewed the product"""
        # create temp account and log-in to it
        user = get_user_model().objects.create_user(
            username=f'test_user@email.com',
            email=f'test_user@email.com',
            password='pass123')
        self.client.force_login(user=user)
        response = self.client.get(self.reverse_url)
        # form will only be displayed if 'display_form' is true
        self.assertTrue('display_form' in response.context)
        self.assertTrue(response.context['display_form'])
        self.assertContains(response, 'Add a product review')

    def test_review_form_does_not_display_user_logged_in(self):
        """When user is logged in and has already reviewed a product,
        review form should not display"""
        response = self.client.get(self.reverse_url)

        user = get_user_model().objects.create_user(
            username='test_user@email.com',
            email='test_user@email.com',
            password='pass123')

        Review.objects.create(product=self.product, rating=3,
                              review='This is a product review.', user=user)

        # user and user review created, now log-in to account and view product
        self.client.force_login(user=user)
        response = self.client.get(self.reverse_url)

        # form will only be displayed if 'display_form' is true
        self.assertTrue('display_form' not in response.context)
        self.assertNotContains(response, 'Add a product review')
        self.assertContains(response, 'You have already submitted a review')

    def test_view_when_no_reviews_for_product(self):
        """Product with no reviews displays correct text"""
        product = Product.objects.create(
            title='New product', brand='product', category='animal',
            price=12.99, stock=11, description='Something',
            image=SimpleUploadedFile(
                name='image.jpg',
                content=open(settings.BASE_DIR +
                             '/test/image.jpg', 'rb').read(),
                content_type='image/jpeg'
            ),
            is_live=True
        )

        response = self.client.get(
            reverse('product_detail', kwargs={'pk': product.id}))

        self.assertContains(
            response, 'This product does not yet have any reviews')
        # checked class does not exist on page (i.e. no reviews left)
        self.assertNotContains(response, 'class="fas fa-star checked"')


class ProductCreateView(TestCase):
    """Product create is an admin view, only users with specified permission
    should be permitted access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user@email.com',
            email='test_user@email.com',
            password='pass123')

        self.manual_url = '/products/create/'
        self.reverse_url = reverse('product_create')

    def test_view_anonymous_user(self):
        """Anonymous user accessing admin page should be redirected to login"""
        response = self.client.get(self.reverse_url)
        # page should be redirected to login (302)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_view_registered_user_no_permission(self):
        """Registered user without specific permission should be forbidden
        from accessing page"""
        self.client.force_login(user=self.user)
        response = self.client.get(self.reverse_url)
        # user access should be forbidden
        self.assertEqual(response.status_code, 403)

    def test_view_registered_user_has_permission_reverse_url(self):
        """Registered user with specific permission should be permitted to
        access page, using reverse url"""
        # add permission to user account
        permission = Permission.objects.get(name='Can add product')
        self.user.user_permissions.add(permission)
        self.client.force_login(user=self.user)

        response = self.client.get(self.reverse_url)
        # page should load successfully
        self.assertContains(response, 'Create')
        self.assertContains(response, 'Is live')
        self.assertContains(response, 'Stock')

    def test_view_registered_user_has_permission_manual_url(self):
        """Registered user with specific permission should be permitted to
        access page, using manual url"""
        # add permission to user account
        permission = Permission.objects.get(name='Can add product')
        self.user.user_permissions.add(permission)
        self.client.force_login(user=self.user)

        response = self.client.get(self.manual_url)
        # page should load successfully
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        """Make sure the correct template is used to render page"""
        permission = Permission.objects.get(name='Can add product')
        self.user.user_permissions.add(permission)
        self.client.force_login(user=self.user)
        response = self.client.get(self.reverse_url)
        self.assertTemplateUsed(response, 'products/product_create.html')


class ProductUpdateView(TestCase):
    """Update product is an admin view, only users with specified permission
    should be permitted access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user@email.com',
            email='test_user@email.com',
            password='pass123')

        self.product_details = {
            'title': 'Doggie Treats',
            'brand': 'Pawful Intentions',
            'category': 'Dog',
            'price': 9.99,
            'stock': 11,
            'description': 'Doggie Treats',
            # simulate the content required for imagefield
            'image': SimpleUploadedFile(
                name='image.jpg',
                content=open(settings.BASE_DIR +
                             '/test/image.jpg', 'rb').read(),
                content_type='image/jpeg'
            ),
            'is_live': True
        }

        self.product = Product.objects.create(**self.product_details)

        self.manual_url = '/products/' + str(self.product.id) + '/update/'
        self.reverse_url = reverse('product_update', kwargs={
                                   'pk': self.product.id})

    def test_view_anonymous_user(self):
        """Anonymous user accessing admin page should be redirected to login"""
        response = self.client.get(self.reverse_url)
        # page should be redirected to login (302)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_view_registered_user_no_permission(self):
        """Registered user without specific permission should be forbidden
        from accessing page"""
        self.client.force_login(user=self.user)
        response = self.client.get(self.reverse_url)
        # user access should be forbidden
        self.assertEqual(response.status_code, 403)

    def test_view_registered_user_has_permission_reverse_url(self):
        """Registered user with specific permission should be permitted to
        access page, using reverse url"""
        # add permission to user account
        permission = Permission.objects.get(name='Can change product')
        self.user.user_permissions.add(permission)
        self.client.force_login(user=self.user)

        response = self.client.get(self.reverse_url)
        # page should load successfully
        self.assertContains(response, 'Update Product Details')
        self.assertContains(response, self.product.title)
        self.assertContains(response, self.product.description)

    def test_view_registered_user_has_permission_manual_url(self):
        """Registered user with specific permission should be permitted to
        access page, using manual url"""
        # add permission to user account
        permission = Permission.objects.get(name='Can change product')
        self.user.user_permissions.add(permission)
        self.client.force_login(user=self.user)

        response = self.client.get(self.manual_url)
        # page should load successfully
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        """Make sure the correct template is used to render page"""
        permission = Permission.objects.get(name='Can change product')
        self.user.user_permissions.add(permission)
        self.client.force_login(user=self.user)
        response = self.client.get(self.reverse_url)
        self.assertTemplateUsed(response, 'products/product_update.html')


class ProductDeleteView(TestCase):
    """Delete product is an admin view, only users with specified permission
    should be permitted access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user@email.com',
            email='test_user@email.com',
            password='pass123')

        self.product_details = {
            'title': 'Doggie Treats',
            'brand': 'Pawful Intentions',
            'category': 'Dog',
            'price': 9.99,
            'stock': 11,
            'description': 'Doggie Treats',
            # simulate the content required for imagefield
            'image': SimpleUploadedFile(
                name='image.jpg',
                content=open(settings.BASE_DIR +
                             '/test/image.jpg', 'rb').read(),
                content_type='image/jpeg'
            ),
            'is_live': True
        }

        self.product = Product.objects.create(**self.product_details)

        self.manual_url = '/products/' + str(self.product.id) + '/delete/'
        self.reverse_url = reverse('product_delete', kwargs={
                                   'pk': self.product.id})

    def test_view_anonymous_user(self):
        """Anonymous user accessing admin page should be redirected to login"""
        response = self.client.get(self.reverse_url)
        # page should be redirected to login (302)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_view_registered_user_no_permission(self):
        """Registered user without specific permission should be forbidden
        from accessing page"""
        self.client.force_login(user=self.user)
        response = self.client.get(self.reverse_url)
        # user access should be forbidden
        self.assertEqual(response.status_code, 403)

    def test_view_registered_user_has_permission_reverse_url(self):
        """Registered user with specific permission should be permitted to
        access page, using reverse url"""
        # add permission to user account
        permission = Permission.objects.get(name='Can delete product')
        self.user.user_permissions.add(permission)
        self.client.force_login(user=self.user)

        response = self.client.get(self.reverse_url)
        # page should load successfully
        self.assertContains(response, 'Delete Product')
        self.assertContains(response, 'Are you sure you want to delete')
        self.assertContains(response, self.product.title)

    def test_view_registered_user_has_permission_manual_url(self):
        """Registered user with specific permission should be permitted to
        access page, using manual url"""
        # add permission to user account
        permission = Permission.objects.get(name='Can delete product')
        self.user.user_permissions.add(permission)
        self.client.force_login(user=self.user)

        response = self.client.get(self.manual_url)
        # page should load successfully
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        """Make sure the correct template is used to render page"""
        permission = Permission.objects.get(name='Can delete product')
        self.user.user_permissions.add(permission)
        self.client.force_login(user=self.user)
        response = self.client.get(self.reverse_url)
        self.assertTemplateUsed(response, 'products/product_delete.html')


class ProductSearchResultsView(TestCase):
    """Ensure search view outputs results as expected"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user@email.com',
            email='test_user@email.com',
            password='pass123')

        self.product_details = {
            'title': 'Doggie Treats',
            'brand': 'Pawful Intentions',
            'category': 'Dog',
            'price': 9.99,
            'stock': 11,
            'description': 'Doggie Treats',
            # simulate the content required for imagefield
            'image': SimpleUploadedFile(
                name='image.jpg',
                content=open(settings.BASE_DIR +
                             '/test/image.jpg', 'rb').read(),
                content_type='image/jpeg'
            ),
            'is_live': True
        }

        self.product = Product.objects.create(**self.product_details)

        self.manual_url = '/products/search/'
        self.reverse_url = reverse('product_search')

    def test_view_url_exists(self):
        """Check that the hardcoded page exists"""
        response = self.client.get(self.manual_url)
        self.assertEqual(response.status_code, 200)

    def test_view_reverse_url(self):
        """Check that the named view page exists"""
        response = self.client.get(self.reverse_url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        """Make sure the correct template is used to render page"""
        response = self.client.get(self.reverse_url)
        self.assertTemplateUsed(
            response, 'products/product_search_results.html')

    def test_view_when_no_products_exist_in_db(self):
        """Search should return an expected response when database is empty"""
        # delete all products
        Product.objects.all().delete()
        search_terms = '?keywords=dog'
        response = self.client.get(self.reverse_url + search_terms)
        self.assertContains(
            response, 'Your search did not return any results - please try '
            'another search term')

    def test_view_when_no_search_term(self):
        """When no search keywords are passed, search view should return
        message only"""
        search_terms = '?keywords='
        response = self.client.get(self.reverse_url + search_terms)
        self.assertContains(
            response, 'Your search did not return any results - please try '
            'another search term')

    def test_view_search_term_does_not_match_any_products(self):
        """When search keywords do not match any products, search view should
        return message only"""
        search_terms = '?keywords=dogs'
        response = self.client.get(self.reverse_url + search_terms)
        self.assertContains(
            response, 'Your search did not return any results - please try '
            'another search term')

    def test_view_search_term_matches_products(self):
        """Search term matches products in the database - all products should
        be returned by the view"""
        search_terms = '?keywords=dog'
        response = self.client.get(self.reverse_url + search_terms)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/products/search/')
        self.assertContains(response, '<div class="product">')
        self.assertNotContains(response, 'Your search did not return any '
                               'results - please try another search term')

    def test_view_does_not_show_products_non_live_products(self):
        """Search should not return products where is_live=False"""
        product2_details = {
            'title': 'Non-Live Product',
            'brand': 'Pawful Intentions',
            'category': 'Dog',
            'price': 9.99,
            'stock': 11,
            'description': 'Doggie Treats (not live)',
            # simulate the content required for imagefield
            'image': SimpleUploadedFile(
                name='image.jpg',
                content=open(settings.BASE_DIR +
                             '/test/image.jpg', 'rb').read(),
                content_type='image/jpeg'
            ),
            'is_live': False
        }

        # product2 is_live = False - should not be shown on website
        Product.objects.create(**product2_details)
        # search for the brand of both products - expecting one result
        search_terms = '?keywords=pawful+intentions'
        response = self.client.get(self.reverse_url + search_terms)

        # expect two products, only one on search results page
        number_of_products = Product.objects.all().count()
        self.assertEqual(
            len(response.context['search_results']), number_of_products)
        # make sure new product does not appear on list
        self.assertNotContains(response, product2_details['title'])

    def test_view_pagination(self):
        """Search results should be paginated"""
        # clear products table (remove product created in setUp method)
        Product.objects.all().delete()

        # add products to test pagination
        number_of_products = 9

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
                # simulate the content required for imagefield
                'image': SimpleUploadedFile(
                    name='image.jpg',
                    content=open(settings.BASE_DIR +
                                 '/test/image.jpg', 'rb').read(),
                    content_type='image/jpeg'
                ),
                'is_live': is_live
            }
            Product.objects.create(**product_details)
        search_terms = '?keywords=Pawfect'
        response = self.client.get(self.reverse_url + search_terms)

        # page will only be paginated if number of products created is greater
        # than the pagination number
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['search_results']), 8)
